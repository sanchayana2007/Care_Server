import { DashboardComponent } from './components/dashboard/dashboard.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ElementCoreModule } from './element-core/element-core.module';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AmazingTimePickerModule } from 'amazing-time-picker';
import { ChartsModule } from 'ng2-charts';
import { MatVideoModule } from 'mat-video';
import { QRCodeModule } from 'angularx-qrcode';
import { MatExpansionModule } from '@angular/material/expansion';

import { NgModule } from '@angular/core';
import { SharedModule } from '../../src/app/shared/shared.module';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthorizationComponent } from './authorization/authorization.component';
import { SignInComponent } from './authorization/sign-in/sign-in.component';
import { SignUpComponent } from './authorization/sign-up/sign-up.component';
import {
  MatSidenavModule, MatCardModule, MatDividerModule, MatDatepickerModule,
  MatPaginatorModule, MatTableModule, MatNativeDateModule, MatSnackBarModule,
  MatDialogModule, MatOptionModule, MatSelectModule, MatStepperModule, MatCheckboxModule,
  MatSlideToggleModule, MatRadioModule, MatTabsModule
} from '@angular/material';
import { MatToolbarModule } from '@angular/material/toolbar';
import { ChartModule } from 'angular2-chartjs';
import {
  PerfectScrollbarModule, PerfectScrollbarConfigInterface,
  PERFECT_SCROLLBAR_CONFIG
} from 'ngx-perfect-scrollbar';
import { Router, Routes, RouterModule } from '@angular/router';
import { AUTHGWCONSTANTS } from './authorization/authconstants';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatListModule } from '@angular/material/list';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatTreeModule } from '@angular/material/tree';

import { HttpClientModule } from '@angular/common/http';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { NgxMaskModule, IConfig } from 'ngx-mask';

import { ToasterModule, ToasterService } from 'angular2-toaster';
import { GoogleMapLoaderService } from './other/GoogleMapLoader';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { Ng2OdometerModule } from 'ng2-odometer';
import { ProfileComponent } from './components/profile/profile.component';
import { HelpComponent } from './components/help/help.component';
import { ElementWidgetModule } from './element-widget/element-widget.module';
import { HomePageComponent } from './components/account/home-page/home-page.component';
import { DateFormat } from './other/date-format';
import { DatePipe } from '@angular/common';
import { ServiceOptionsComponent } from './authorization/service-options/service-options.component';
import { DetailsPageComponent } from './components/account/details-page/details-page.component';
import { ServiceProviderComponent } from './components/account/service-provider/service-provider.component';


const DEFAULT_PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
  suppressScrollX: false,
  suppressScrollY: false
};

const routes: Routes = [
  {
    path: 'admin',
    component: AuthorizationComponent
  },
  {
    path: 'sign_in',
    component: SignInComponent
  },
  {
    path: 'sign_up',
    component: SignUpComponent
  },
];

const maskConfig: Partial<IConfig> = {
  validation: false,
};

@NgModule({
  declarations: [
    DateFormat,
    AppComponent,
    AuthorizationComponent,
    DashboardComponent,
    SignInComponent,
    SignUpComponent,
    // Dialogs
    ProfileComponent,
    HelpComponent,

    HomePageComponent,
    ServiceOptionsComponent,
    DetailsPageComponent,
    ServiceProviderComponent,
  ],
  entryComponents: [
    ProfileComponent,
    HelpComponent,
  ],
  imports: [
    ElementCoreModule,
    BrowserModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatDividerModule,
    MatPaginatorModule,
    MatTableModule,
    MatIconModule,
    MatCheckboxModule,
    MatRadioModule,
    MatSlideToggleModule,
    FormsModule,
    MatExpansionModule,
    // AuthConstants,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatNativeDateModule,
    ChartModule,
    MatVideoModule,
    FlexLayoutModule,
    MatDatepickerModule,
    MatListModule,
    MatTabsModule,
    MatSnackBarModule,
    MatOptionModule,
    MatSelectModule,
    MatDialogModule,
    MatSidenavModule,
    MatToolbarModule,
    MatTreeModule,
    SharedModule,
    PerfectScrollbarModule,
    AppRoutingModule,
    AmazingTimePickerModule,
    OwlNativeDateTimeModule,
    ChartsModule,
    ElementCoreModule,
    ElementWidgetModule,
    HttpClientModule,
    OwlDateTimeModule,
    MatProgressBarModule,
    // DashboardWidgetModule,
    Ng2OdometerModule,
    MatStepperModule,
    MatTooltipModule,
    QRCodeModule,
    ToasterModule.forRoot(),
    RouterModule.forRoot(routes),
    NgxMaskModule.forRoot(maskConfig)
  ],
  providers: [
    DatePipe,
    {
      provide: PERFECT_SCROLLBAR_CONFIG,
      useValue: DEFAULT_PERFECT_SCROLLBAR_CONFIG
    },
    {
      provide: LocationStrategy,
      useClass: HashLocationStrategy
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(private router: Router) {
    // Google custom map loader
    GoogleMapLoaderService.load().then(() => { });
    if (!window.location.hash.includes('ex/')) {
      if (
        localStorage.getItem(AUTHGWCONSTANTS.bearerToken) === 'null' ||
        localStorage.getItem(AUTHGWCONSTANTS.bearerToken) === null
      ) {
        localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
        this.router.navigate(['sign_in']);
      } else {
        // this.router.navigate(['admin/dashboard']);
        this.router.navigate(['service-types']);
        // this.router.navigate(['tourist-form']);
        // this.router.navigate(['provider-form']);
      }
    }
  }
}
