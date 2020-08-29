import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { ServiceProviderService } from '../service-provider.service';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
@Component({
  selector: 'app-service-provider-service-info-dialong',
  templateUrl: './service-provider-service-info-dialong.component.html',
  styleUrls: ['./service-provider-service-info-dialong.component.scss'],
  providers: [ServiceProviderService]
})
export class ServiceProviderServiceInfoDialongComponent implements OnInit {

  data: any;
  title: string;
  file_name: any;
  loadServiceImage = false;
  formData: any = null;
  address: any;
  buttonHide = false;
  constructor(public thisDialogRef: MatDialogRef<ServiceProviderServiceInfoDialongComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any, private snackBar: MatSnackBar,
    private service: ServiceProviderService, breakpointObserver: BreakpointObserver) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;
    this.title = 'Service Provider Details';


  }

  ngOnInit() {
    this.getServices();
  }
  getServices() {
    this.service.getServiceDetails(this.data.id).subscribe(success => {
      if (success.status) {
        this.loadServiceDetails(success.result);
      }
    });
  }
  loadServiceDetails(data): void {
    this.data = data;
    if (this.data !== undefined && this.data !== null
      && this.data.length !== 0) {
      for (let i = 0; i < this.data.length; i++) {
        if (this.data[i].serviceName === undefined ||
          this.data[i].serviceName === null ||
          this.data[i].serviceName === '') {
          this.data[i].serviceName = 'N/A';
        } else {
          this.data[i].serviceName = this.data[i].serviceName;
        }
        if (this.data[i].media[0].link === undefined ||
          this.data[i].media[0].link === null ||
          this.data[i].media[0].link === '') {
          this.data[i].imageurl = 'N/A';
        } else {
          this.data[i].imageurl = this.data[i].media[0].link;
        }
        if (this.data[i].status === undefined ||
          this.data[i].status === null ||
          this.data[i].status === '') {
          this.data[i].status = '';
        } else {
          this.data[i].status = this.data[i].status;
          if (this.data[i].status === true) {
            this.data[i].status = 'Accepted';
          } else if (this.data[i].status === false) {
            this.data[i].status = 'Rejected';
          }
        }
      }
    }
  }
  onAccept(id) {
    const body = {
      statusValue: true,
      providerService: id
    };
    this.service.addServiceList(body).subscribe(success => {
      if (success.status) {
        this.getServices();
        this.openSuccessSnackBar(success.message);
       // this.onClose();
      } else {
        this.openErrorSnackBar(success.message);
      }
    }, error => {
      this.openErrorSnackBar(error.code + ': HTTP ERROR IN POST BOOKING CONFIRM ACCEPT');
    });
  }

  onDecline(id) {
    const body = {
      statusValue: false,
      providerService: id
    };
    this.service.addServiceList(body).subscribe(success => {
      if (success.status) {
        this.getServices();
        this.openSuccessSnackBar(success.message);
        // this.onClose();
        
      } else {
        this.openErrorSnackBar(success.message);
      }
    }, error => {
      this.openErrorSnackBar(error.code + ': HTTP ERROR IN POST BOOKING CONFIRM DECLINE');
    });
  }


  onClose(): void {
    ServiceProviderService.dialogResult = false;
    this.thisDialogRef.close();
  }

  openErrorSnackBar(message: string) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }
}
