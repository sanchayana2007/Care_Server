import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBarConfig } from '@angular/material';
import { MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { Router } from '@angular/router';
import { AccountInfoService } from '../account-info.service';

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss'],
  providers: [AccountInfoService]
})
export class DetailsPageComponent implements OnInit {

  headingText = true;

  serviceInfoIcon = true;
  pendingVerified = true;
  progressBarValue = 0;
  matProgressBar = true;
  activationTitleGreen = true;
  activationTitleRed = true;
  data = {
    phoneNumber_text: '',
    submmitedCount: 0,
  };
  id = sessionStorage.getItem('id');
  constructor(private snackBar: MatSnackBar, private service: AccountInfoService,
    private router: Router) {
    ToolbarHelpers.toolbarTitle = 'Service Registration';
  }

  ngOnInit() {
    this.getHomePage();
  }

  getHomePage() {
    this.service.getHomePage(this.id).subscribe(success => {
      console.log('homepage details', success);
      if (success.status) {
        try {
          if (success.result.length > 0) {
            const value1 = success.result;
            if (value1.length > 0) {
              const value = value1[0];
              if (value.serviceProvider === true) {
                this.serviceInfoIcon = false;
                this.data.submmitedCount++;
                this.progressBarValue = (100 + this.progressBarValue);
              }
              if (value.verified === true) {
                this.pendingVerified = false;
              }
            }
          }
        } catch (e) {
          // console.log(e);
        }
      }
    });
  }
  onServiceProvider() {
    this.router.navigate(['account/service-provider']);
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
