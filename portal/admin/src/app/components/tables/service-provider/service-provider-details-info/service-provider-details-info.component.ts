import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { ServiceProviderService } from '../service-provider.service';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
@Component({
  selector: 'app-service-provider-details-info',
  templateUrl: './service-provider-details-info.component.html',
  styleUrls: ['./service-provider-details-info.component.scss'],
  providers: [ServiceProviderService]
})
export class ServiceProviderDetailsInfoComponent implements OnInit {

  data: any;
  title: string;
  file_name: any;
  loadServiceImage = false;
  formData: any = null;
  address: any;
  buttonHide = false;
  displayedColumns: string[] = [
    'fullName', 'address', 'actions'
  ];
  constructor(public thisDialogRef: MatDialogRef<ServiceProviderDetailsInfoComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any, private snackBar: MatSnackBar,
    private service: ServiceProviderService, breakpointObserver: BreakpointObserver) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;
    this.title = 'Service Provider Details';
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['fullName', 'address', 'actions'];
    });
    console.log(this.data);
    if (this.data !== null) {
      this.address = this.data.address;
      this.buttonHide = this.data.verified;
      if (this.data.document !== '') {
        this.data.image_url = this.data.document[0].link;
      }
      if (this.data.declaration !== '') {
        this.data.image_url1 = this.data.declaration[0].link;
      }
    }
  }

  ngOnInit() {

  }
  onAccept() {
    const body = {
      statusValue: true,
      id: this.data.id
    };
    this.service.addServiceList(body).subscribe(success => {
      if (success.status) {
        this.openErrorSnackBar(success.message);
        this.onClose();
      } else {
        this.openErrorSnackBar(success.message);
      }
    }, error => {
      this.openErrorSnackBar(error.code + ': HTTP ERROR IN POST BOOKING CONFIRM ACCEPT');
    });
  }

  onDecline() {
    const body = {
      statusValue: false,
      id: this.data.id
    };
    this.service.addServiceList(body).subscribe(success => {
      if (success.status) {
        this.openErrorSnackBar(success.message);
        this.onClose();
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
