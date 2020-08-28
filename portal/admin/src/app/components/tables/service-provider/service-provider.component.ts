import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ServiceProviderService } from './service-provider.service';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import {ServiceProviderDetailsInfoComponent} from './service-provider-details-info/service-provider-details-info.component';
import { dataLoader } from '@amcharts/amcharts4/core';
import {ServiceProviderServiceInfoDialongComponent} from './service-provider-service-info-dialong/service-provider-service-info-dialong.component';

@Component({
  selector: 'app-admin',
  templateUrl: './service-provider.component.html',
  styleUrls: ['./service-provider.component.scss'],
  providers: [ServiceProviderService]
})
export class ServiceProviderComponent implements OnInit {

  displayedColumns: string[] = [
    'full_name', 'contact_number', 'address','district', 'qualification', 'actions'
  ];
  dataSource: MatTableDataSource<any>;
  searchOpen = false;
  adminTable = true;
  loadAdmin = false;
  selectedservice= false;
  defaultSelectedService = '';
  errorMessage: string;
  componentClosed = false;
  componentClosedTitle = 'Enabled';
  componentClosedValue = 0;
  isMobile = true;
  serviceList: any;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: ServiceProviderService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['full_name', 'contact_number', 'address','district', 'qualification', 'actions'];
    });
    ToolbarHelpers.toolbarTitle = 'Provider';
  }

  ngOnInit() {
    this.getServices();
    this.onChange(event);
  }

  onChange(event) {
    if (event.checked === false) {
      this.componentClosed = false;
      this.componentClosedTitle = 'Enabled';
      this.componentClosedValue = 0;
      // this.onGetServiceList();
    } else if (event.checked === true) {
      this.componentClosed = true;
      this.componentClosedTitle = 'Disabled';
      this.componentClosedValue = 1;
      // this.onGetServiceList();
    }
  }
  getServices() {
    this.loadAdmin = true;
    this.service.getService_list().subscribe(data => {
      if (data.status) {
        this.serviceList = data.result;
      }
    });
    this.service.getServices().subscribe(success => {
      try {
        if (success.status) {
          this.loadServiceData(success.result);
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
  onGetServiceList(): void {
    this.loadAdmin = true;
    this.service.getServiceList(this.defaultSelectedService, this.componentClosedValue)
    .subscribe(success => {
      try {
        if (success.status) {
          this.loadServiceData(success.result);
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

  loadServiceData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].fullName === undefined || data[i].fullName === null ||
            data[i].fullName === '') {
            data[i].full_name_text = 'N/A';
          } else {
            data[i].full_name_text = data[i].fullName;
          }
          if (data[i].registeredPhoneNum === undefined
            || data[i].registeredPhoneNum === 0) {
            data[i].contact_number_text = 'N/A';
          } else {
            data[i].contact_number_text = data[i].registeredPhoneNum;
          }
          if (data[i].address === undefined || data[i].address === null ||
            data[i].address === '') {
            data[i].address_text = 'N/A';
          } else {
            data[i].address_text = data[i].address;
          }
          if (data[i].district === undefined || data[i].district === null ||
            data[i].district === '') {
            data[i].district_text = 'N/A';
          } else {
            data[i].district_text = data[i].district;
          }
          if (data[i].qualification === undefined || data[i].qualification === null ||
            data[i].qualification === '') {
            data[i].squalification_text = 'N/A';
          } else {
            data[i].qualification_text = data[i].qualification;
          }
          if (data[i].verified === undefined || data[i].verified === null ||
            data[i].verified === '') {
            data[i].verified_text = 'N/A';
          } else {
            data[i].verified_text = data[i].verified;
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
  onSelectedServiceChange(event: any): void {
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getServices();
    this.onChange(event);
    this.openDefaultSnackBar('Refreshing ....');
  }

  onBasicDetails(element) {
    const data = {
      dialog_data: element,
    };
    this.openBasicDetailsDialog(data);
  }
  onServicDetails(element) {
    const data = {
      dialog_data: element,
    };
    this.openServiceDetailsDialog(data);
  }


  onDelete(id) {
    this.openErrorSnackBar('Do not delete the Admin');
  }

  openBasicDetailsDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '800px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ServiceProviderDetailsInfoComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      // if (ServiceProviderService.dialogResult) {
      //   this.getAdmins();
      // } else {
      //   // closed
      // }
    });
  }
  openServiceDetailsDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '800px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ServiceProviderServiceInfoDialongComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      // if (ServiceProviderService.dialogResult) {
      //   this.getAdmins();
      // } else {
      //   // closed
      // }
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
