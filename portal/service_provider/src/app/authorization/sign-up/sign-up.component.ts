import { Component, OnInit } from '@angular/core';
import { AUTHGWCONSTANTS } from '../authconstants';
import { Router } from '@angular/router';
import { AuthorizationService } from '../authorization.service';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss'],
  providers: [AuthorizationService]
})
export class SignUpComponent implements OnInit {

  title: string;
  firstName_text = '';
  lastName_text = '';
  phoneNumber_text = '';
  email_text = '';
  otp_text = '';
  submitDiv = true;
  verifyOtp = true;

  constructor(private authService: AuthorizationService, private router: Router,
    private snackBar: MatSnackBar) {
    this.title = 'REGISTER';
  }

  ngOnInit() {
    this.phoneNumber_text = sessionStorage.getItem('phoneNumber');
  }

  onSubmit() {
    if (this.isValid()) {
      const body = {
        applicationId: environment.applicationId,
        method: 1,
        countryCode: 91,
        firstName: this.firstName_text,
        lastName: this.lastName_text,
        phoneNumber: this.phoneNumber_text,
        email: this.email_text,
      };
      this.authService.postSignUp(body).subscribe(success => {
        if (success.status) {
          if (this.authService.updateHeaders()) {
            // this.router.navigate(['admin/dashboard']);
            this.title = 'OTP';
            this.verifyOtp = false;
            this.submitDiv = false;
          }
          this.openSuccessSnackBar(success.message);
        } else {
          this.openErrorSnackBar(success.message);
        }
      });
    } else {
    }
  }

  verify() {
    if (this.otp_text === '') {
      this.openErrorSnackBar('Enter your Otp');
      return;
    } else {
      const body = {
        applicationId: environment.applicationId,
        method: 1,
        countryCode: 91,
        otp: this.otp_text,
        phoneNumber: this.phoneNumber_text,
      };
      this.authService.putOtp(body).subscribe(success => {
        if (success.status) {
          localStorage.setItem(AUTHGWCONSTANTS.bearerToken, success.result[0].bearerToken);
          localStorage.setItem(AUTHGWCONSTANTS.xApiKey, success.result[0].apiKey);
          if (this.authService.updateHeaders()) {
            // this.router.navigate(['admin/dashboard']);
            this.router.navigate(['service-types']);
          }
          this.openSuccessSnackBar(success.message);
        } else {
          this.openErrorSnackBar(success.message);
        }
      });
    }
  }

  onBack() {
    this.router.navigate(['sign_in']);
    sessionStorage.removeItem('phoneNumber');
  }

  isValid(): boolean {
    if (this.firstName_text === null || this.firstName_text === '') {
      this.openErrorSnackBar('Enter your First Name');
      return false;
    }
    if (this.lastName_text === null || this.lastName_text === '') {
      this.openErrorSnackBar('Enter your Last Name');
      return false;
    }
    if (this.phoneNumber_text === null || this.phoneNumber_text === '') {
      this.openErrorSnackBar('Enter your Phone Number');
      return false;
    }
    return true;
  }

  openSuccessSnackBar(message: string) {
    const config = new MatSnackBarConfig();
    config.verticalPosition = 'bottom';
    config.horizontalPosition = 'right';
    config.panelClass = ['snakbar-class-success'];
    config.duration = 3000;
    this.snackBar.open(message, ' ', config);
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
