import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { AUTHGWCONSTANTS } from '../../../../authorization/authconstants';
import { ProdectsService } from '../prodects.service';

@Component({
  selector: 'app-prodects-add-dialog',
  templateUrl: './prodects-add-dialog.component.html',
  styleUrls: ['./prodects-add-dialog.component.scss']
})
export class ProdectsAddDialogComponent implements OnInit {
  data: any;
  productTable = true;
  ServiceList: any;
  dialogState = 0;
  title: any;

  constructor(public thisDialogRef: MatDialogRef<ProdectsAddDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private dailogData: any, private service: ProdectsService,
    private snackBar: MatSnackBar) {
    this.dailogData = JSON.stringify(this.dailogData);
    this.dailogData = JSON.parse(this.dailogData);
    this.data = this.dailogData.dialog_data;

    if (this.data) {
      console.log(this.data.serviceName, 'edit data', this.data);
      this.dialogState = 1;
      this.title = 'Edit Product';
      this.data.serviceId = this.data.serviceId,
        this.data.productName = this.data.productName,
        this.data.productPrice = this.data.productPrice;
      console.log(this.data.serviceId);
    } else {
      this.dialogState = 2;
      this.title = 'Add Product';
      this.data = {};
      this.data.serviceId = 0,
        this.data.productName = '',
        this.data.productPrice = '';
    }
  }

  ngOnInit() {
    this.getServiceList();
  }
  onSave(): void {
    console.log(this.dialogState);
    if (this.dialogState === 2) {
      const body = {
        serviceId: this.data.serviceId,
        productName: this.data.productName,
        productPrice: Number(this.data.productPrice)
      };
      this.service.addProduct(body).subscribe(success => {
        if (success.status) {
          ProdectsService.dialogResult = true;
          this.thisDialogRef.close();
          this.getServiceList();
          this.openSuccessSnackBar(success.message);
        } else {
          ProdectsService.dialogResult = false;
          this.openErrorSnackBar(success.message);
        }
      }, error => {
        ProdectsService.dialogResult = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD ADMIN');
      });
    } else if (this.dialogState === 1) {
      const body = {
        productId: this.data.id,
        serviceId: this.data.serviceId,
        productName: this.data.productName,
        productPrice: Number(this.data.productPrice)
      };
      console.log(body, 'edit');
      this.service.editProduct(body).subscribe(success => {
        if (success.status) {
          ProdectsService.dialogResult = true;
          this.thisDialogRef.close();
          this.openSuccessSnackBar(success.message);
        } else {
          ProdectsService.dialogResult = false;
          this.openErrorSnackBar(success.message);
        }
      }, error => {
        ProdectsService.dialogResult = false;
        this.openErrorSnackBar(error.status + ': HTTP ERROR IN ADD ADMIN');
      });
    }
  }
  getServiceList(): void {
    this.service.getServiceList().subscribe(success => {
      if (success.status) {
        this.ServiceList = success.result;
      } else {
        this.productTable = false;
      }
    });
  }
  onClose(): void {
    ProdectsService.dialogResult = false;
    this.thisDialogRef.close();
  }
  openErrorSnackBar(message: string, ) {
    const config = new MatSnackBarConfig<any>();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 5000;
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
}
