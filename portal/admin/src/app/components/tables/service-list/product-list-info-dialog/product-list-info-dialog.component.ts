import { Component, OnInit, ViewChild , Inject} from '@angular/core';
import { MatDialogRef, MatPaginator, MatTableDataSource, MAT_DIALOG_DATA, MatSnackBar } from '@angular/material';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { ServiceListService } from '../service-list.service';

@Component({
  selector: 'app-product-list-info-dialog',
  templateUrl: './product-list-info-dialog.component.html',
  styleUrls: ['./product-list-info-dialog.component.scss']
})
export class ProductListInfoDialogComponent implements OnInit {
  displayedColumns: string[] = [
    'product_name', 'product_price'
  ];
  data: any;
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
  
  constructor( public thisDialogRef: MatDialogRef<ProductListInfoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dialogData: any, private snackBar: MatSnackBar,
    breakpointObserver: BreakpointObserver, private service: ServiceListService) {
      breakpointObserver.observe(['(max-width: 0px)']).subscribe(result => {
        this.displayedColumns = result.matches ?
          [] :
          ['product_name', 'product_price'];
      });
    this.dialogData = JSON.stringify(this.dialogData);
    this.dialogData = JSON.parse(this.dialogData);
    this.data = this.dialogData.dialog_data;
    this.loadProdectData(this.data);
    }


  ngOnInit() {

  }

  loadProdectData(data: any) {
    try {
      if (data !== undefined && data !== null
        && data.length !== 0) {
        for (let i = 0; i < data.length; i++) {
          
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

  onClose(): void {
    ServiceListService.dialogResult = false;
    this.thisDialogRef.close();
  }
}
