import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { AccountInfoService } from '../account-info.service';
@Component({
  selector: 'app-my-services',
  templateUrl: './my-services.component.html',
  styleUrls: ['./my-services.component.scss'],
  providers: [AccountInfoService]
})
export class MyServicesComponent implements OnInit {

  displayedColumns: string[] = [
    'serNameEnglish', 'serNameHindi', 'serCharge'
  ];
  dataSource: MatTableDataSource<any>;
  title: string;
  searchOpen = false;
  loadServiceList = false;
  dialogResult = '';
  serviceListTable = true;
  errorMessage: string;
  // componentDisabled = false;
  // componentDisabledTitle = 'Enabled';
  // componentDisabledValue = 0;
  isMobile = true;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: AccountInfoService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['serNameEnglish', 'serNameHindi', 'serCharge'];
    });
    ToolbarHelpers.toolbarTitle = 'Service List';
  }

  ngOnInit() {
    this.getServiceList();
    // this.onChange(event);
  }

    getServiceList() {
    this.loadServiceList = true;
    this.service.getMyservices().subscribe(success => {
      console.log(success.result);
      try {
        if (success.status) {
          this.loadServiceListData(success.result);
        } else {
          this.serviceListTable = false;
          this.errorMessage = (success.code + ': ' + success.message).toUpperCase();
        }
      } catch (e) {
        this.serviceListTable = false;
        this.errorMessage = '1001: SERVER ERROR';
      }
      this.loadServiceList = false;
    }, error => {
      this.loadServiceList = false;
      this.openErrorSnackBar(error.status + ': HTTP ERROR IN GET SERVICE LIST');
    });
  }

  loadServiceListData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].serviceName === undefined || data[i].serviceName === null ||
            data[i].serviceName === '') {
            data[i].serviceName_text = 'N/A';
          } else {
            data[i].serviceName_text = data[i].serviceName;
          }
          if (data[i].totalBookings === undefined || data[i].totalBookings === null ||
            data[i].totalBookings === '') {
            data[i].totalBookings_text = 'N/A';
          } else {
            data[i].totalBookings_text = data[i].totalBookings;
          }
          if (data[i].status === undefined || data[i].status === null ||
            data[i].status === '') {
            data[i].status_text = '';
          } else {
            if (data[i].status === true) {
              data[i].status_text = 'Approved';
            } else if (data[i].status === false) {
              data[i].status_text = 'Rejected';
            }
          }
        }
        this.serviceListTable = true;
        this.dataSource = new MatTableDataSource<any>(data);
        this.dataSource.paginator = this.paginator;
      } else {
        this.serviceListTable = false;
        this.dataSource = new MatTableDataSource<any>([]);
        this.dataSource.paginator = this.paginator;
        this.errorMessage = '1002: NO DATA AVAILABLE';
      }
    } catch (e) {
      this.serviceListTable = false;
      this.errorMessage = '1003: DATA LOAD ERROR';
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getServiceList();
    // this.onChange(event);
    this.openDefaultSnackBar('Refreshing ....');
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
