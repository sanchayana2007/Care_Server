import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { MatDialogConfig, MatDialog } from '@angular/material';
import { ServiceOptionsService } from './service-options.service';
import { environment } from 'src/environments/environment';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { AreYouSureDialogComponent } from 'src/app/element-widget/are-you-sure-dialog/are-you-sure-dialog.component';
import { from } from 'rxjs';

@Component({
  selector: 'app-service-options',
  templateUrl: './service-options.component.html',
  styleUrls: ['./service-options.component.scss'],
  providers: [ServiceOptionsService]
})
export class ServiceOptionsComponent implements OnInit {

  data: any;
  title: string;
  Image1: string;
  Image2: string;
  Image3: string;
  Image4: string;
  Image5: string;

  constructor(private service: ServiceOptionsService, private router: Router,
    public dialog: MatDialog, private snackBar: MatSnackBar) {
    // ToolbarHelpers.toolbarTitle = 'SERVICE TYPES';
    // ToolbarHelpers.areYouSureTitle = 'You are not registered for this service,' + ' ' +
    //   'would you like to register for this service?';
    // console.log(this.accomodationUrl);
  }

  ngOnInit() {
    this.getServiceTypes();
  }

  getServiceTypes() {
    this.service.getServiceTypes().subscribe(success => {
      console.log(success);
      if (success.status) {
        this.data = success.result;
          this.Image1 = this.data[0].media[0].link;
           this.Image2 = this.data[1].media[0].link;
           this.Image3 = this.data[2].media[0].link;
           this.Image4 = this.data[3].media[0].link;
           this.Image5 = this.data[4].media[0].link;
        // if (this.data[1].serviceType === 2 && this.data[1].active === true) {
        //   this.tourGuideColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/Named/TourGuide.png';
        // } else if (this.data[1].serviceType === 2 && this.data[1].active === false) {
        //   this.tourGuideColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/grayscale/TourGuide.png';
        // }

        // if (this.data[2].serviceType === 3 && this.data[2].active === true) {
        //   this.tourOperatorColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/Named/TourOperator.png';
        // } else if (this.data[2].serviceType === 3 && this.data[2].active === false) {
        //   this.tourOperatorColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/grayscale/TourOperator.png';
        // }

        // if (this.data[3].serviceType === 4 && this.data[3].active === true) {
        //   this.transportColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/Named/transport.png';
        // } else if (this.data[3].serviceType === 4 && this.data[3].active === false) {
        //   this.transportColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/grayscale/transport.png';
        // }

        // if (this.data[4].serviceType === 5 && this.data[4].active === true) {
        //   this.boatmanColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/Named/BoatMan.png';
        // } else if (this.data[4].serviceType === 5 && this.data[4].active === false) {
        //   this.boatmanColorBlackUrl = environment.proxyApiUrl +
        //   '/uploads/icons/meghalayaIcons/grayscale/Boatman.png';
        // }
      } else {
        this.openErrorSnackBar(success.message);
      }
    });
  }


  onServiceOptions(value: number): void {
    try {
      if (this.data !== undefined && this.data !== null &&
        this.data.length !== 0) {
          sessionStorage.setItem('id', this.data[value]._id);
        if (value === 0 ) {
          this.router.navigate(['account/details-page']);
        } else if (value === 0 ) {
          this.router.navigate(['account/details-page']);
          // this.openAreYouSureDialog(this.data);
        } else if (value === 1 ) {
          this.router.navigate(['account/details-page']);
        } else if (value === 1 ) {
          // this.openAreYouSureDialog(this.data);
          this.router.navigate(['account/details-page']);
        } else if (value === 2 ) {
          this.router.navigate(['account/details-page']);
        } else if (value === 2) {
          // this.openAreYouSureDialog(this.data);
          this.router.navigate(['account/details-page']);
        } else if (value === 3) {
          this.router.navigate(['account/details-page']);
        } else if (value === 3 ) {
          // this.openAreYouSureDialog(this.data);
          this.router.navigate(['account/details-page']);
        } else if (value === 4) {
          this.router.navigate(['account/details-page']);
        } else if (value === 4 ) {
          // this.openAreYouSureDialog(this.data);
          this.router.navigate(['account/details-page']);
        }
      } else {
        // tslint:disable-next-line:no-console
        console.log('NO SERVICE TYPE');
      }
    } catch (e) {
      // tslint:disable-next-line:no-console
      console.log('DATA LOAD ERROR');
    }
  }
  openErrorSnackBar(message: string) {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-error'];
    config.duration = 3000;
    this.snackBar.open(message, ' ', config);
  }
}
