import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource, MatSnackBarConfig } from '@angular/material';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { ProdectsService } from './prodects.service';
import {ProdectsAddDialogComponent} from './prodects-add-dialog/prodects-add-dialog.component';

@Component({
  selector: 'app-prodects',
  templateUrl: './prodects.component.html',
  styleUrls: ['./prodects.component.scss'],
  // providers: [ProdectsService]
})
export class ProdectsComponent implements OnInit {

  displayedColumns: string[] = [
    'service_name', 'product_name', 'product_price', 'actions'
  ];
  dataSource: MatTableDataSource<any>;
  searchOpen = false;
  productTable = true;
  loadProduct = false;
  errorMessage: string;
  componentClosed = false;
  componentClosedTitle = 'Enabled';
  componentClosedValue = 0;
  isMobile = true;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar,
    private service: ProdectsService, breakpointObserver: BreakpointObserver
  ) {
    breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
      this.displayedColumns = result.matches ?
        [] :
        ['service_name', 'product_name', 'product_price', 'actions'];
    });
    ToolbarHelpers.toolbarTitle = 'Admins';
  }

  ngOnInit() {
    this.getProdect();
  }


  getProdect() {
    this.loadProduct = true;
    this.service.getProdectList().subscribe(success => {
      console.log(success, 'success')
      try {
        if (success.status) {
          this.loadProdectData(success.result);
        } else {
          this.productTable = false;
          this.errorMessage = (success.code + ': ' + success.message).toUpperCase();
        }
      } catch (e) {
        this.productTable = false;
        this.errorMessage = '1001: INVALID RESPONSE';
      }
      this.loadProduct = false;
    },
      error => {
        this.loadProduct = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN GET ADMIN');
      }
    );
  }

  loadProdectData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].serviceName === undefined || data[i].serviceName === null ||
            data[i].serviceName === '') {
            data[i].full_name_text = 'N/A';
          } else {
            data[i].full_name_text = data[i].serviceName;
          }
          if (data[i].productName === undefined || data[i].productName === null ||
            data[i].productName === '') {
            data[i].productName_text = 'N/A';
          } else {
            data[i].productName_text = data[i].productName;
          }
          if (data[i].productPrice === undefined || data[i].productPrice === null ||
            data[i].productPrice === '') {
            data[i].productPrice_text = 'N/A';
          } else {
            data[i].productPrice_text = data[i].productPrice;
          }
        }
        this.productTable = true;
        this.dataSource = new MatTableDataSource<any>(data);
        this.dataSource.paginator = this.paginator;
      } else {
        this.productTable = false;
        this.dataSource = new MatTableDataSource<any>([]);
        this.dataSource.paginator = this.paginator;
        this.errorMessage = '1002: NO DATA AVAILABLE';
      }
    } catch (e) {
      this.productTable = false;
      this.errorMessage = '1003: DATA LOAD ERROR';
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onRefresh() {
    this.getProdect();
    this.openDefaultSnackBar('Refreshing ....');
  }

  onCreate() {
    const data = {
      dialog_data: null,
    };
    this.openAddDialog(data);
    console.log('on create', data);
  }
  openAddDialog(data): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.panelClass = ['dialog-class'];
    dialogConfig.height = 'auto';
    dialogConfig.width = '600px';
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(ProdectsAddDialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe(result => {
      // if (ServiceProviderService.dialogResult) {
      //   this.getAdmins();
      // } else {
      //   // closed
      // }
    });
  }
  onEdit(element) {
    const data = {
      dialog_data: element,
    };
    this.openAddDialog(data);
    console.log('on Edit', data);
  }

  onDelete(id) {
    console.log(id);
    this.service.deleteProduct(id).subscribe(success => {
      if (success.status) {
        this.openSuccessSnackBar(success.message);
      } else {
        this.openErrorSnackBar(success.message);
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
  openSuccessSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
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
