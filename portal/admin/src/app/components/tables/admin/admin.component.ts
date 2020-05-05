import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { AdminDialogComponent } from './admin-dialog/admin-dialog.component';
import { AdminService } from './admin.service';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
  providers: [AdminService]
})
export class AdminComponent implements OnInit {

  displayedColumns: string[] = [
    'full_name', 'contact_number', 'email', 'actions'
  ];
  dataSource: MatTableDataSource<any>;
  searchOpen = false;
  adminTable = true;
  loadAdmin = false;
  errorMessage: string;
  componentClosed = false;
  componentClosedTitle = 'Enabled';
  componentClosedValue = 0;
  isMobile = true;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: AdminService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['full_name', 'contact_number', 'email', 'actions'];
    });
    ToolbarHelpers.toolbarTitle = 'Admins';
  }

  ngOnInit() {
    this.getAdmins();
    this.onChange(event);
  }

  onChange(event) {
    if (event.checked === false) {
      this.componentClosed = false;
      this.componentClosedTitle = 'Enabled';
      this.componentClosedValue = 0;
      this.getAdmins();
    } else if (event.checked === true) {
      this.componentClosed = true;
      this.componentClosedTitle = 'Disabled';
      this.componentClosedValue = 1;
      this.getAdmins();
    }
  }

  getAdmins() {
    this.loadAdmin = true;
    this.service.getAdmins(this.componentClosedValue).subscribe(success => {
      try {
        if (success.status) {
          this.lodAdminsData(success.result);
        } else {
          this.adminTable = false;
          this.errorMessage = (success.code + ': ' + success.message).toUpperCase();
        }
      } catch (e) {
        this.adminTable = false;
        this.errorMessage = '1001: INVALID RESPONSE';
      }
      this.loadAdmin = false;
    },
      error => {
        this.loadAdmin = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN GET ADMIN');
      }
    );
  }

  lodAdminsData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].firstName === undefined || data[i].firstName === null ||
            data[i].firstName === '') {
            data[i].full_name_text = 'N/A';
          } else if (data[i].lastName === undefined || data[i].lastName === null ||
            data[i].lastName === '') {
            data[i].full_name_text = 'N/A';
          } else {
            data[i].full_name_text = data[i].firstName + ' ' + data[i].lastName ;
          }
          if (data[i].contact.length === undefined || data[i].contact.length === 0) {
            data[i].contact_number_text = 'N/A';
          } else {
            data[i].contact_number_text = data[i].contact[0].value;
          }
          if (data[i].contact.length === undefined || data[i].contact.length === 0 ||
            data[i].contact.length < 2) {
            data[i].email_text = 'N/A';
          } else {
            data[i].email_text = data[i].contact[1].value;
          }
        }
        this.adminTable = true;
        this.dataSource = new MatTableDataSource<any>(data);
        this.dataSource.paginator = this.paginator;
      } else {
        this.adminTable = false;
        this.dataSource = new MatTableDataSource<any>([]);
        this.dataSource.paginator = this.paginator;
        this.errorMessage = '1002: NO DATA AVAILABLE';
      }
    } catch (e) {
      this.adminTable = false;
      this.errorMessage = '1003: DATA LOAD ERROR';
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getAdmins();
    this.onChange(event);
    this.openDefaultSnackBar('Refreshing ....');
  }

  onCreate() {
    const data = {
      dialog_data: null,
    };
    this.openDialog(data);
  }

  onEdit(element) {
    const data = {
      dialog_data: element,
    };
    this.openDialog(data);
  }

  onDelete(id) {
    this.openErrorSnackBar('Do not delete the Admin');
    // if (window.confirm('Are you sure you want to delete?')) {
    //   this.service.deleteAdmins(id).subscribe(
    //     success => {
    //       if (success.status) {
    //         this.onRefresh();
    //       }
    //     },
    //     error => {

    //     }
    //   );
    // } else {

    // }
  }

  openDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '600px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(AdminDialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (AdminService.dialogResult) {
        this.getAdmins();
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
