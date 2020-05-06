import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { ServiceListService } from './service-list.service';
import { ServiceListDialogComponent } from './service-list-dialog/service-list-dialog.component';
import { ServiceImageUploadDialogComponent } from './service-image-upload-dialog/service-image-upload-dialog.component';

@Component({
  selector: 'app-service-list',
  templateUrl: './service-list.component.html',
  styleUrls: ['./service-list.component.scss'],
  providers: [ServiceListService]
})
export class ServiceListComponent implements OnInit {

  displayedColumns: string[] = [
    'serNameEnglish', 'serNameHindi', 'serCharge', 'serTaDa', 'serCharge', 'serTotalAmount',
    'actions'
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
  default_image = './../../../../../assets/images/avatars/upload_image.png';

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: ServiceListService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['serNameEnglish', 'serNameHindi', 'serCharge', 'serTaDa', 'serTotalAmount',
        'actions'];
    });
    ToolbarHelpers.toolbarTitle = 'Service List';
  }

  ngOnInit() {
    this.getServiceList();
    // this.onChange(event);
  }

  // onChange(event) {
  //   if (event.checked === false) {
  //     this.componentDisabled = false;
  //     this.componentDisabledTitle = 'Enabled';
  //     this.componentDisabledValue = 0;
  //     this.getServiceList();
  //   } else if (event.checked === true) {
  //     this.componentDisabled = true;
  //     this.componentDisabledTitle = 'Disabled';
  //     this.componentDisabledValue = 1;
  //     this.getServiceList();
  //   }
  // }


  getServiceList() {
    this.loadServiceList = true;
    this.service.getServiceList().subscribe(success => {
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
          if (data[i].serNameEnglish === undefined || data[i].serNameEnglish === null ||
            data[i].serNameEnglish === '') {
            data[i].serviceNameEnglish_text = 'N/A';
          } else {
            data[i].serviceNameEnglish_text = data[i].serNameEnglish;
          }
          if (data[i].serNameHindi === undefined || data[i].serNameHindi === null ||
            data[i].serNameHindi === '') {
            data[i].serviceNameHindi_text = 'N/A';
          } else {
            data[i].serviceNameHindi_text = data[i].serNameHindi;
          }
          if (data[i].serCharges === undefined || data[i].serCharges === null ||
            data[i].serCharges === 0) {
            data[i].serviceCharge_text = 0;
          } else {
            data[i].serviceCharge_text = data[i].serCharges;
          }
          if (data[i].serTA === undefined || data[i].serTA === null ||
            data[i].serTA === 0) {
            data[i].serviceTA_text = 0;
          } else {
            data[i].serviceTA_text = data[i].serTA;
          }
          // if (data[i].serDA === undefined || data[i].serDA === null ||
          //   data[i].serDA === 0) {
          //   data[i].serviceDA_text = 0;
          // } else {
          //   data[i].serviceDA_text = data[i].serDA;
          // }
          if (data[i].serTATotal === undefined || data[i].serTATotal === null ||
            data[i].serTATotal === 0) {
            data[i].serviceTAtotal_text = 0;
          } else {
            data[i].serviceTAtotal_text = data[i].serTATotal;
          }
          // if (data[i].serDATotal === undefined || data[i].serDATotal === null ||
          //   data[i].serDATotal === 0) {
          //   data[i].serviceDAtotal_text = 0;
          // } else {
          //   data[i].serviceDAtotal_text = data[i].serDATotal;
          // }
          if (data[i].media.length === undefined || data[i].media.length === null ||
            data[i].media.length === 0 || data[i].media[0].link === '') {
            data[i].serviceImage = this.default_image;
          } else {
            data[i].serviceImage = data[i].media[0].link;
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

  onCreate() {
    const data = {
      dialog_data: null,
    };
    this.openDialog(data);
  }

  serviceImageUpload(element) {
    const data = {
      dialog_data: element,
    };
    this.openServiceImageUploadDialog(data);
  }

  onEdit(element) {
    const data = {
      dialog_data: element,
    };
    this.openDialog(data);
  }

  onDelete(_id) {
    if (window.confirm('Are you sure you want to delete?')) {
      this.service.deleteServiceList(_id).subscribe(success => {
        if (success.status) {
          this.openErrorSnackBar(success.message);
          this.onRefresh();
        }
      },
        error => {

        }
      );
    } else {
    }
  }

  openDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '600px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ServiceListDialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (ServiceListService.dialogResult) {
        this.getServiceList();
      } else {
        // closed
      }
    });
  }

  openServiceImageUploadDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '600px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ServiceImageUploadDialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      if (ServiceListService.dialogResult) {
        // this.getServiceList();
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

