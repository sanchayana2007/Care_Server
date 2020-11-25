import { Component, OnInit, Inject } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { AppointmentsService } from '../appointments.service';
@Component({
  selector: 'app-assingdoctordialog',
  templateUrl: './assingdoctordialog.component.html',
  styleUrls: ['./assingdoctordialog.component.scss']
})
export class AssingdoctordialogComponent implements OnInit {
  data: any;
  id: any;
  serviceProviderId: any;
  constructor(
    public thisDialogRef: MatDialogRef<AssingdoctordialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dialogData: any, private snackBar: MatSnackBar,
    private service: AppointmentsService) {
    this.dialogData = JSON.stringify(this.dialogData);
    this.dialogData = JSON.parse(this.dialogData);
    this.id = this.dialogData.dialog_data.serviceId;
    this.serviceProviderId = '';
  }

  ngOnInit() {
    this.ongetDoctorlist();
  }
  ongetDoctorlist(): void {
    this.service.asigndoctor(this.id).subscribe(
      success => {
        console.log(success);
        if (success.status) {
          this.data = success.result;
        }
      });
  }
  onClose(): void {
    AppointmentsService.dialogResult = false;
    this.thisDialogRef.close();
  }
  onSave(): void {
    const body = {
      serviceProviderId: this.serviceProviderId,
      id: this.dialogData.dialog_data._id
    };
    console.log(body);
    this.service.AssignDoctor(body).subscribe(
      success => {
        console.log(success);
        if ((success.status)) {
          AppointmentsService.dialogResult = true;
          this.thisDialogRef.close();
          this.openSuccessSnackBar(success.message);
        } else {
          AppointmentsService.dialogResult = false;
          this.openErrorSnackBar(success.message);
        }
      },
      error => {
        AppointmentsService.dialogResult = false;

        this.openErrorSnackBar(
          error.status + ': HTTP ERROR IN EDIT APPOINTMENT STAGE'
        );
      }
    );
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
