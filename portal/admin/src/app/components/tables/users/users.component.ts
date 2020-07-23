import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { UsersService } from './users.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {

  
  displayedColumns: string[] = [
    'full_name', 'contact_number', 'bookingCount' 
  ];
  dataSource: MatTableDataSource<any>;
  searchOpen = false;
  userTable = true;
  loadUsers = false;
  errorMessage: string;
  componentClosed = false;
  componentClosedTitle = 'Enabled';
  componentClosedValue = 0;
  isMobile = true;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: UsersService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['full_name', 'contact_number', 'bookingCount'];
    });
    ToolbarHelpers.toolbarTitle = 'Users';
  }

  ngOnInit() {
    this.getUsers();
    //this.onChange(event);
  }
/*
  onChange(event) {
    if (event.checked === false) {
      this.componentClosed = false;
      this.componentClosedTitle = 'Enabled';
      this.componentClosedValue = 0;
      this.getUsers();
    } else if (event.checked === true) {
      this.componentClosed = true;
      this.componentClosedTitle = 'Disabled';
      this.componentClosedValue = 1;
      this.getUsers();
    }
  }
  */

  getUsers() {
    this.loadUsers = true;
    this.service.getUsers().subscribe(success => {
      console.log(success);
      try {
        if (success.status) {
          this.loadUsersData(success.result);
          this.loadUsers = false;
        } else {
          this.userTable = false;
          this.errorMessage = (success.code + ': ' + success.message).toUpperCase();
        }
      } catch (e) {
        this.userTable = false;
        this.errorMessage = '1001: INVALID RESPONSE';
      }
      this.loadUsers = false;
    },
      error => {
        this.loadUsers = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN GET ADMIN');
      }
    );
  }

  loadUsersData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
          if (data[i].fullName === undefined || data[i].fullName === null ||
            data[i].fullName === '') {
            data[i].fullName = 'N/A';
          } else {
            data[i].fullName = data[i].fullName;
          }
          if (data[i].phoneNumber === undefined || data[i].phoneNumber === 0) {
            data[i].phoneNumber = 'N/A';
          } else {
            data[i].phoneNumber = data[i].phoneNumber;
          }
          if (data[i].bookingCount === undefined || data[i].bookingCount === 0 ) {
            data[i].bookingCount = '0';
          } else {
            data[i].bookingCount = data[i].bookingCount;
          }
        }
        this.userTable = true;
        this.dataSource = new MatTableDataSource<any>(data);
        this.dataSource.paginator = this.paginator;
      } else {
        this.userTable = false;
        this.dataSource = new MatTableDataSource<any>([]);
        this.dataSource.paginator = this.paginator;
        this.errorMessage = '1002: NO DATA AVAILABLE';
      }
    } catch (e) {
      this.userTable = false;
      this.errorMessage = '1003: DATA LOAD ERROR';
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getUsers();
    //this.onChange(event);
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
 //   const dialogRef = this.dialog.open(AdminDialogComponent, dialogConfig);
   // dialogRef.afterClosed().subscribe(result => {
     // if (UsersService.dialogResult) {
        this.getUsers();
      //} else {
        // closed
     // }
    //});
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

