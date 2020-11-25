import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { AccountInfoService } from '../account-info.service';
import { AppointmentsPreviewComponent} from './appointments-preview/appointments-preview.component';
import { AppointmentsDialogComponent } from './appointments-dialog/appointments-dialog.component';
import * as moment from 'moment';
@Component({
  selector: 'app-my-bookings',
  templateUrl: './my-bookings.component.html',
  styleUrls: ['./my-bookings.component.scss']
})
export class MyBookingsComponent implements OnInit {

  displayedColumns: string[] = [
    'requestedDateTime', 'coustomerName', 'contactNumber',
    'email', 'serviceName', 'stage', 'actions'
  ];
  dataSource: MatTableDataSource<any>;
  title: string;
  searchOpen = false;
  loadAppointments = false;
  dialogResult = '';
  appointmentsTable = true;
  errorMessage: string;
  element: string;
  isMobile = true;
  value: boolean;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: AccountInfoService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['requestedDateTime', 'coustomerName', 'contactNumber',
         'serviceName', 'stage', 'session', 'actions'];
    });
    ToolbarHelpers.toolbarTitle = 'Appointments';
  }

  ngOnInit() {
    this.getAppointments();
  }

  getAppointments() {
    this.loadAppointments = true;
    this.service.getAppointments().subscribe(success => {

      try {
        if (success.status) {
          this.loadAppointmentsData(success.result);
        } else {
          this.appointmentsTable = false;
          this.errorMessage = (success.code + ': ' + success.message).toUpperCase();
        }
      } catch (e) {
        this.appointmentsTable = false;
        this.errorMessage = '1001: SERVER ERROR';
      }
      this.loadAppointments = false;
    }, error => {
      this.loadAppointments = false;
      this.openErrorSnackBar(error.status + ': HTTP ERROR IN GET APPOINTMENTS');
    });
  }

  onOrderInfo(element) {
    this.element = element;
    const data = {
      dialog_data: element
    };
    this.openDownloadDialog(data);
  }
  openDownloadDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = '100%';
    dialogConfig.width = '100%';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(AppointmentsPreviewComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (AccountInfoService.dialogResult) {
        this.getAppointments();
      } else {
        // closed
      }
    });
  }
  loadAppointmentsData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].requestedTime === undefined || data[i].requestedTime === 0 ||
            data[i].requestedTime === '') {
            data[i].requestedDateTime_text = 'N/A';
          } else {
            data[i].requestedDateTime_text = moment.unix(data[i].requestedTime / 1000000)
            .format(' hh:mm A DD/MM/YYYY');
          }
          if (data[i].booktime === undefined || data[i].booktime === 0 ||
            data[i].booktime === '') {
            data[i].bookingDateTime_text = 'N/A';
          } else {
            data[i].bookingDateTime_text = moment.unix(data[i].booktime / 1000000)
            .format(' hh:mm A DD/MM/YYYY');
          }
          if (data[i].accountDetails.length === undefined || data[i].accountDetails.length === 0 ||
            data[i].accountDetails[0].firstName === '' ||
            data[i].accountDetails[0].lastName === '') {
            data[i].fullName_text = 'N/A';
          } else {
            data[i].fullName_text = data[i].accountDetails[0].firstName + ' ' +
            data[i].accountDetails[0].lastName;
          }
          if (data[i].accountDetails.length === 0 ||
            data[i].accountDetails[0].contact.length === undefined ||
            data[i].accountDetails[0].contact.length === 0) {
              data[i].contact_number_text = 'N/A';
          } else {
            data[i].contact_number_text = data[i].accountDetails[0].contact[0].value - 910000000000;
          }
          if (data[i].serviceDetails.length === undefined || data[i].serviceDetails.length === 0 ||
            data[i].serviceDetails[0].serNameEnglish === '') {
            data[i].serviceNameEnglish_text = 'N/A';
          } else {
            data[i].serviceNameEnglish_text = data[i].serviceDetails[0].serNameEnglish;
          }
          if (data[i].stage === undefined || data[i].stage === null ||
            data[i].stage === '') {
            data[i].stage_text = 'N/A';
          } else {
            data[i].stage_text = data[i].stage;
          }
          if (data[i].session === undefined || data[i].session === null ||
            data[i].session === '') {
            data[i].session = 'N/A';
          } else {
            data[i].session = data[i].session;
          }
          if (data[i].session_remaining === undefined || data[i].session_remaining === null ||
            data[i].session_remaining === '') {
            data[i].session_remaining = 'N/A';
          } else {
            data[i].session_remaining = data[i].session_remaining;
          }
          if (data[i].serviceProvider === undefined || data[i].serviceProvider === null ||
            data[i].serviceProvider === '') {
            data[i].serviceProvider_text = '';
          } else {
            data[i].serviceProvider_text = data[i].serviceProvider;
          }
          if (data[i].serviceDetails.length === undefined || data[i].serviceDetails.length === 0 ||
            data[i].serviceDetails[0].serTATotal === '') {
            data[i].serviceDetails[0].serTATotal = 'N/A';
          } else {
            data[i].serviceDetails[0].serTATotal = data[i].serviceDetails[0].serTATotal;
          }
        }
        this.appointmentsTable = true;
        this.dataSource = new MatTableDataSource<any>(data);
        this.dataSource.paginator = this.paginator;
      } else {
        this.appointmentsTable = false;
        this.dataSource = new MatTableDataSource<any>([]);
        this.dataSource.paginator = this.paginator;
        this.errorMessage = '1002: NO DATA AVAILABLE';
      }
    } catch (e) {
      this.appointmentsTable = false;
      this.errorMessage = '1003: DATA LOAD ERROR';
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getAppointments();
    this.openDefaultSnackBar('Refreshing ....');
  }

  onDateTime(element) {
    if (element.stage_text === 'completed') {
      this.openDefaultSnackBar('Appointment already completed ');
    } else {
      const data = {
        dialog_data: element,
        value: 1
      };
      this.openDialog(data);
    }
  }

  onEdit(element) {
    if (element.stage_text === 'completed') {
      this.openDefaultSnackBar('Appointment already completed ');
    } else {
      const data = {
        dialog_data: element,
        value: 2
      };
      this.openDialog(data);
    }
  }

  // onDelete(_id) {
  //   if (window.confirm('Are you sure you want to delete?')) {
  //     this.service.deleteAppointments(_id).subscribe(success => {
  //       if (success.status) {
  //         this.openErrorSnackBar(success.message);
  //         this.onRefresh();
  //       }
  //     },
  //       error => {

  //       }
  //     );
  //   } else {
  //   }
  // }
  
  onSession(element) {
    if (element.stage_text === 'completed' && element.session_remaining === 0) {
      this.openDefaultSnackBar('Appointment already completed ');
    } else if (element.stage_text === 'new' ) {
      this.openDefaultSnackBar('Please accept the Appointment');
    } else if (element.stage_text === 'declined' || element.stage_text === 'declined_fee' ) {
      this.openDefaultSnackBar('The Appointment has been cancelled.');
    } else {
      this.service.sessionupdate(element._id).subscribe(success => {
        if (success.status) {
          this.onRefresh();
        }
      },
        error => {

        }
      );
    }
  }

  openDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '700px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(AppointmentsDialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (AccountInfoService.dialogResult) {
        this.getAppointments();
      } else {
        // closed
      }
    });
  }

  openDefaultSnackBar(message: string) {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-default'];
    config.duration = 800;
    this.snackBar.open(message, 'Close', config);
  }

  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
    this.snackBar.open(message, 'Close', config);
  }
}