import { Component, OnInit, Inject } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig } from '@angular/material';
import { ServiceListService } from '../service-list.service';

@Component({
  selector: 'app-service-list-dialog',
  templateUrl: './service-list-dialog.component.html',
  styleUrls: ['./service-list-dialog.component.scss'],
  providers: [ServiceListService]
})
export class ServiceListDialogComponent implements OnInit {

  data: any;
  title: string;
  loadServiceList = false;
  dialogState = 0;

  constructor( public thisDialogRef: MatDialogRef<ServiceListDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dialogData: any, private snackBar: MatSnackBar,
    private service: ServiceListService) {
    this.dialogData = JSON.stringify(this.dialogData);
    this.dialogData = JSON.parse(this.dialogData);
    this.data = this.dialogData.dialog_data;

    if (this.data) {
      this.dialogState = 2;
      this.title = 'Edit Service List Details';
    } else {
      this.dialogState = 1;
      this.title = 'Add Service List Details';
      this.data = {};
      this.data.serviceNameEnglish_text = '';
      this.data.serviceNameHindi_text = '';
      this.data.serviceTaDa_text = '';
      this.data.serviceCharge_text = '';
      this.data.serviceTotal_text = '';
    }
  }

  ngOnInit() {

  }

  onClose(): void {
    ServiceListService.dialogResult = false;
    this.thisDialogRef.close();
  }

  onSave() {
    if (this.isValid()) {
      this.loadServiceList = true;
      if (this.dialogState === 2) {
        const body = {
          serviceId: this.data.id,
          serNameEnglish: this.data.serviceNameEnglish_text,
          serNameHindi: this.data.serviceNameHindi_text,
          serTADA: this.data.serviceTaDa_text,
          serCharges: this.data.serviceCharge_text,
        };
        this.service.editServiceList(body).subscribe(success => {
          if (success.status) {
            ServiceListService.dialogResult = true;
            this.thisDialogRef.close();
            this.openSuccessSnackBar(success.message);
          } else {
            ServiceListService.dialogResult = false;
            this.openErrorSnackBar(success.message);
          }
          this.loadServiceList = false;
        }, error => {
          ServiceListService.dialogResult = false;
          this.loadServiceList = false;
          this.openErrorSnackBar(error.status + ': HTTP ERROR IN EDIT SERVICE LIST');
        });
      } else if (this.dialogState === 1) {
        const body = {
          serNameEnglish: this.data.serviceNameEnglish_text,
          serNameHindi: this.data.serviceNameHindi_text,
          serTADA: this.data.serviceTaDa_text,
          serCharges: this.data.serviceCharge_text,
        };
        this.service.addServiceList(body).subscribe(success => {
          if (success.status) {
            ServiceListService.dialogResult = true;
            this.thisDialogRef.close();
            this.openSuccessSnackBar(success.message);
          } else {
            ServiceListService.dialogResult = false;
            this.openErrorSnackBar(success.message);
          }
          this.loadServiceList = false;
        }, error => {
          ServiceListService.dialogResult = false;
          this.loadServiceList = false;
          this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD SERVICE LIST');
        });
      }
    }
  }

  isValid(): boolean {
    if (this.data.serviceNameEnglish_text === null || this.data.serviceNameEnglish_text === '') {
      this.openErrorSnackBar('Enter a Service Name English');
      return false;
    }
    if (this.data.serviceNameHindi_text === null || this.data.serviceNameHindi_text === '') {
      this.openErrorSnackBar('Enter a Service Name Hindi');
      return false;
    }
    if (this.data.serviceTaDa_text === null || this.data.serviceTaDa_text === '') {
      this.openErrorSnackBar('Enter a Service TA/DA');
      return false;
    }
    if (this.data.serviceCharge_text === null || this.data.serviceCharge_text === '') {
      this.openErrorSnackBar('Enter a Service Charge');
      return false;
    }
    return true;
  }

  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }

  openSuccessSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, 'Close', config);
  }
}

