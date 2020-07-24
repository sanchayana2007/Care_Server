import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBarConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { Router } from '@angular/router';
import { AccountInfoService } from '../account-info.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
  providers: [AccountInfoService],
})
export class HomePageComponent implements OnInit {

  leasedProp = true;
  nextButton = false;
  activation = true;
  firstStage = true;
  covid19Stage = true;
  qrCodeStage = true;
  public scanQrCode: string = null;
  data = {
    phoneNumber_text: '',
    submmitedCount: 0,
    tableCount: 0,
    // covid19_text: '',
    activation_text: '',
    totalCount: 9
  };

  constructor(private snackBar: MatSnackBar, private service: AccountInfoService,
    private router: Router) {
    ToolbarHelpers.toolbarTitle = 'HOME PAGE';
  }

  ngOnInit() {
    this.getHomePage();
  }

  getHomePage() {
    this.service.getHomePage(1).subscribe(success => {
      if (success.status) {
        try {
          if (success.result.length > 0) {
            const value1 = success.result;
            if (value1.length > 0) {
              const value = value1[0];
              if (value.provideraccountDetails[0].contact.length === undefined ||
                value.provideraccountDetails[0].contact.length === 0) {
                this.data.phoneNumber_text = 'N/A';
              } else {
                this.data.phoneNumber_text = value.provideraccountDetails[0].contact[0].value;
                this.scanQrCode = String(value.provideraccountDetails[0].contact[0].value);
              }
              if (value.propertyInfo.length > 0) {
                this.data.submmitedCount++;
              }
              if (value.hotelInfo.length > 0) {
                this.data.submmitedCount++;
              }
              if (value.invInfo.length > 0) {
                this.data.submmitedCount++;
              }
              if (value.amenities.length > 0) {
                this.data.submmitedCount++;
              }
              if (value.empInfo.length > 0) {
                this.data.submmitedCount++;
              }
              if (value.Fin2017.length > 0 || value.Fin2018.length > 0 ||
                value.Fin2019.length > 0) {
                  this.data.submmitedCount++;
              }
              if (value.Rev2017.length > 0 || value.Rev2018.length > 0 ||
                value.Rev2019.length > 0) {
                  this.data.submmitedCount++;
              }
              if (value.docGST.length > 0 || value.docTin.length > 0 ||
                value.docFoodSafety.length > 0 || value.docBarLicense.length > 0 ||
                value.docHotelRegistration.length > 0 || value.docMunicipalHolding.length > 0 ||
                value.docPFAccount.length > 0 || value.docFireSafetyPermit.length > 0 ||
                value.docTradeLicense.length > 0 || value.docESIRegistration.length > 0 ||
                value.docPollutionCertificate.length > 0) {
                  this.data.submmitedCount++;
              }
              if (value.docGST.length > 0 || value.docTin.length > 0 ||
                value.docFoodSafety.length > 0 || value.docBarLicense.length > 0 ||
                value.docHotelRegistration.length > 0 || value.docMunicipalHolding.length > 0 ||
                value.docPFAccount.length > 0 || value.docFireSafetyPermit.length > 0 ||
                value.docTradeLicense.length > 0 || value.docESIRegistration.length > 0 ||
                value.docPollutionCertificate.length > 0) {
                  this.data.submmitedCount++;
              }
              if (value.image1.length > 0 || value.image2.length > 0 ||
                value.image3.length > 0 || value.image4.length > 0 ||
                value.image5.length > 0 || value.image6.length > 0 ||
                value.image7.length > 0 || value.image8.length > 0 ||
                value.image9.length > 0 || value.image10.length > 0) {
                  this.data.submmitedCount++;
              }
              if (this.data.submmitedCount < 7) {
                this.data.tableCount = this.data.submmitedCount;
                return;
              }
              if (this.data.submmitedCount >= 7 && value.covid19Declaration === false) {
                this.firstStage = false;
                this.covid19Stage = false;
                // this.data.covid19_text = 'Your COVID-19 declaration is Pending.';
                return;
              }
              if (value.verified === false) {
                this.firstStage = false;
                this.qrCodeStage = false;
                this.data.activation_text = 'Activation is Pending.';
                return;
              } else if (value.verified === true) {
                this.firstStage = false;
                this.qrCodeStage = false;
                this.activation = false;
              }
            }
          }
        } catch (e) {
          // console.log(e);
        }
      } else {
        this.getAdminProfileInfo();
      }
    });
  }

  // Extra API
  getAdminProfileInfo() {
    this.service.getAdminProfileInfo().subscribe(success => {
      if (success.status) {
        const phoneNumber = success.result[0];
        this.data.phoneNumber_text = phoneNumber.contact[0].value;
        this.scanQrCode = String(phoneNumber.contact[0].value);
        setTimeout(() => {
        }, 400);
      }
    },
      error => {
      }
    );
  }

  onCovid19() {
    this.router.navigate(['account/covid19-declaration']);
  }

  onServiceRegistration() {
    this.router.navigate(['account/property-info']);
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


