import { Component, OnInit, Inject } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { AppointmentsService } from '../appointments.service';

@Component({
  selector: 'app-appointments-dialog',
  templateUrl: './appointments-dialog.component.html',
  styleUrls: ['./appointments-dialog.component.scss'],
  providers: [AppointmentsService]
})
export class AppointmentsDialogComponent implements OnInit {

  data: any;
  title: string;
  loadAppointment = false;
  disabledStatus = true;
  disabledStage = true;
  disabledBookTime = true;
  stageFormField = true;
  dialogState = 0;
  public selectedMomentOne = new Date();
  public selectedMomentTwo = new Date();
  stageData = [
    {
      type: 'accepted',
      value: 'accepted'
    },
    {
      type: 'declined',
      value: 'declined'
    },
    {
      type: 'completed',
      value: 'completed'
    }
  ];

  constructor(
    public thisDialogRef: MatDialogRef<AppointmentsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dialogData: any, private snackBar: MatSnackBar,
    private service: AppointmentsService) {
    this.dialogData = JSON.stringify(this.dialogData);
    this.dialogData = JSON.parse(this.dialogData);
    this.data = this.dialogData.dialog_data;

    if (this.data !== null) {
      if (this.dialogData.value === 1) {
        this.dialogState = 1;
        this.disabledBookTime = false;
        this.title = 'Update Appointment Date/Time';
        this.selectedMomentOne = new Date(this.data.requestedTime / 1000);
        this.selectedMomentTwo = new Date(this.data.booktime / 1000);
      } else {
        this.dialogState = 2;
        this.disabledStage = false;
        this.stageFormField = false;
        this.title = 'Edit Appointment Stage';
        this.selectedMomentOne = new Date(this.data.requestedTime / 1000);
        this.selectedMomentTwo = new Date(this.data.booktime / 1000);
      }
    }
  }

  ngOnInit() {

  }

  onClose(): void {
    AppointmentsService.dialogResult = false;
    this.thisDialogRef.close();
  }

  onSave() {
    if (this.isValid()) {
      this.loadAppointment = true;
      if (this.dialogState === 1) {
        const bookingTime = this.selectedMomentTwo.getTime();
        const body = {
          bookingId: this.data._id,
          booktime: bookingTime * 1000
        };
        this.service.addAppointments(body).subscribe(
          success => {
            if ((success.status)) {
              AppointmentsService.dialogResult = true;
              this.thisDialogRef.close();
              this.openSuccessSnackBar(success.message);
            } else {
              AppointmentsService.dialogResult = false;
              this.openErrorSnackBar(success.message);
            }
            this.loadAppointment = false;
          },
          error => {
            AppointmentsService.dialogResult = false;
            this.loadAppointment = false;
            this.openErrorSnackBar(
              error.status + ': HTTP ERROR IN UPDATE APPOINTMENT DATE TIME'
            );
          }
        );
      } else if (this.dialogState === 2) {
        const body = {
          bookingId: this.data._id,
          stage: this.data.stage_text
        };
        this.service.editAppointments(body).subscribe(
          success => {
            if ((success.status)) {
              AppointmentsService.dialogResult = true;
              this.thisDialogRef.close();
              this.openSuccessSnackBar(success.message);
            } else {
              AppointmentsService.dialogResult = false;
              this.openErrorSnackBar(success.message);
            }
            this.loadAppointment = false;
          },
          error => {
            AppointmentsService.dialogResult = false;
            this.loadAppointment = false;
            this.openErrorSnackBar(
              error.status + ': HTTP ERROR IN EDIT APPOINTMENT STAGE'
            );
          }
        );
      }
    }
  }

  isValid(): boolean {
    if (this.dialogState === 2) {
      if (this.data.stage_text === 'new') {
        this.openErrorSnackBar('Select Appointment Stage');
        return false;
      }
    } else if (
      this.selectedMomentOne.getTime() > this.selectedMomentTwo.getTime() ||
      this.selectedMomentOne.getTime() === this.selectedMomentTwo.getTime()) {
      this.openErrorSnackBar('Invalid date and time is selected');
      return false;
    }
    return true;
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
