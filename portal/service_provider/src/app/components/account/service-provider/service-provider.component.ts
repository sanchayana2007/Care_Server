import { Component, OnInit } from '@angular/core';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { ToolbarHelpers } from 'src/app/element-core/toolbar/toolbar.helpers';
import { AccountInfoService } from '../account-info.service';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { environment } from 'src/environments/environment';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { identifierModuleUrl } from '@angular/compiler';

@Component({
  selector: 'app-service-provider',
  templateUrl: './service-provider.component.html',
  styleUrls: ['./service-provider.component.scss'],
  providers: [AccountInfoService]
})
export class ServiceProviderComponent implements OnInit {

  public static covid19Dec = 0;
  accServiceType: string;
  providerUrl: string;
  urlSafe: any;
  urlChangeCount = 0;

  constructor(private snackBar: MatSnackBar, private service: AccountInfoService,
    private router: Router, public sanitizer: DomSanitizer) {
    const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    const xOriginKey = environment.xOrigin.key;
    const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    const id = sessionStorage.getItem('id');
    this.providerUrl = environment.proxyApiUrl +
      '/provider?' + 'Authorization=' + token +
      '&x-Origin-Key=' + xOriginKey +
      '&x-Api-Key=' + xApiKey +
      '&id=' + id;
    ToolbarHelpers.toolbarTitle = 'Service provider';
    this.urlSafe = this.sanitizer.bypassSecurityTrustResourceUrl(this.providerUrl);
  }

  ngOnInit() {
  }

  iframeclick() {
    try {
      this.urlChangeCount++;
      if (this.urlChangeCount === 3) {
        this.router.navigate(['account/details-page']);
      }
      // console.log(this.urlSafe.changingThisBreaksApplicationSecurity);
      // console.log(myIframe.contentWindow.location.href);
    } catch (e) {

    }
  }

  // openErrorSnackBar(message: string, ) {
  //   const config = new MatSnackBarConfig<any>();
  //   config.verticalPosition = 'bottom';
  //   config.horizontalPosition = 'right';
  //   config.panelClass = ['snakbar-class-error'];
  //   config.duration = 5000;
  //   this.snackBar.open(message, 'Close', config);
  // }

  // openSuccessSnackBar(message: string, ) {
  //   const config = new MatSnackBarConfig<any>();
  //   config.verticalPosition = 'bottom';
  //   config.horizontalPosition = 'right';
  //   config.panelClass = ['snakbar-class-success'];
  //   config.duration = 3000;
  //   this.snackBar.open(message, 'Close', config);
  // }
}
