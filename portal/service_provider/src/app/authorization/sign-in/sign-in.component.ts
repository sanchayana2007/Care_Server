import { Component, OnInit } from '@angular/core';
import { AUTHGWCONSTANTS } from '../authconstants';
import { Router } from '@angular/router';
import { AuthorizationService } from '../authorization.service';
import { MatSnackBarConfig, MatSnackBar } from '@angular/material';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
  providers: [AuthorizationService]
})
export class SignInComponent implements OnInit {

  passwordHide = true;
  title: string;
  verifyOtp = true;
  signInUpdiv = true;
  phoneNumber_text = '';
  otp_text = '';
  user_id = '';
  password = '';
  curr_focus = '';

  constructor(private authService: AuthorizationService, private router: Router,
    private snackBar: MatSnackBar) {
        this.title = 'SIGN IN';
    }

  ngOnInit() {
    const the = this;
    document.addEventListener('keypress', function (event: any) {
      if (event.keyCode === 13) {
        if (the.curr_focus === 'u_id') {
          document.getElementById('pass').focus();
        } else if (the.curr_focus === 'password') {
          the.onSignIn();
        }
      }
    });
  }

  onSignIn() {
    if (this.phoneNumber_text === '') {
      this.openErrorSnackBar('Enter your Phone Number');
      return;
    } else {
      const body = {
        applicationId: environment.applicationId,
        method: 1,
        countryCode: 91,
        phoneNumber: this.phoneNumber_text,
      };
      // sessionStorage.getItem('data');
      this.authService.postSignIn(body).subscribe(success => {
        if (success.code === 4210) {
          sessionStorage.setItem('phoneNumber', this.phoneNumber_text);
          this.router.navigate(['sign_up']);
        }
        if (success.status) {
          if (this.authService.updateHeaders()) {
            // this.router.navigate(['admin/dashboard']);
            this.title = 'OTP';
            this.verifyOtp = false;
            this.signInUpdiv = false;
          }
          this.openSuccessSnackBar(success.message);
        } else {
          this.openErrorSnackBar(success.message);
        }
      });
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

  onSignUp() {
    this.router.navigate(['sign_up']);
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

