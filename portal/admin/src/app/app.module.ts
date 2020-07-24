import { DashboardComponent } from './components/dashboard/dashboard.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ElementCoreModule } from './element-core/element-core.module';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AmazingTimePickerModule } from 'amazing-time-picker';
import { ChartsModule } from 'ng2-charts';

import { NgModule } from '@angular/core';
import { SharedModule } from '../../src/app/shared/shared.module';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthorizationComponent } from './authorization/authorization.component';
import { SignInComponent } from './authorization/sign-in/sign-in.component';
import { SignUpComponent } from './authorization/sign-up/sign-up.component';
import { MatSidenavModule, MatCardModule, MatDividerModule, MatDatepickerModule,
  MatPaginatorModule, MatTableModule, MatNativeDateModule, MatSnackBarModule,
  MatDialogModule, MatOptionModule, MatSelectModule, MatStepperModule, MatCheckboxModule,
  MatSlideToggleModule, MatRadioModule, MatTabsModule } from '@angular/material';
import { MatToolbarModule } from '@angular/material/toolbar';
import { ChartModule } from 'angular2-chartjs';
import { PerfectScrollbarModule, PerfectScrollbarConfigInterface,
  PERFECT_SCROLLBAR_CONFIG } from 'ngx-perfect-scrollbar';
import { Router, Routes, RouterModule } from '@angular/router';
import { AUTHGWCONSTANTS } from './authorization/authconstants';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { AdminComponent } from './components/tables/admin/admin.component';
import { LiveTrackComponent } from './components/live-track/live-track.component';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatListModule } from '@angular/material/list';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatTreeModule } from '@angular/material/tree';

import { HttpClientModule } from '@angular/common/http';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AdminDialogComponent
} from './components/tables/admin/admin-dialog/admin-dialog.component';
import { ToasterModule, ToasterService } from 'angular2-toaster';
import { GoogleMapLoaderService } from './other/GoogleMapLoader';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { Ng2OdometerModule } from 'ng2-odometer';
import { ProfileComponent } from './components/profile/profile.component';
import { HelpComponent } from './components/help/help.component';
import { ElementWidgetModule } from './element-widget/element-widget.module';
import { ServiceListComponent } from './components/tables/service-list/service-list.component';
import { ServiceListDialogComponent } from './components/tables/service-list/service-list-dialog/service-list-dialog.component';
import { AppointmentsComponent } from './components/tables/appointments/appointments.component';
import { AppointmentsDialogComponent } from './components/tables/appointments/appointments-dialog/appointments-dialog.component';
import { ServiceImageUploadDialogComponent } from './components/tables/service-list/service-image-upload-dialog/service-image-upload-dialog.component';
import { AppointmentsPreviewComponent } from './components/tables/appointments/appointments-preview/appointments-preview.component';
import { ServiceProviderComponent } from './components/tables/service-provider/service-provider.component';
import { ServiceProviderDetailsInfoComponent } from './components/tables/service-provider/service-provider-details-info/service-provider-details-info.component';
import {UsersComponent} from './components/tables/users/users.component'

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
    path: 'admin/sign_in',
    component: SignInComponent
  },
];

@NgModule({
  declarations: [
    AppComponent,
    AuthorizationComponent,
    DashboardComponent,
    LiveTrackComponent,
    SignInComponent,
    SignUpComponent,
    AdminComponent,
    // Dialogs
    AdminDialogComponent,
    ProfileComponent,
    HelpComponent,
    UsersComponent,
    ServiceListComponent,
    ServiceListDialogComponent,
    AppointmentsComponent,
    AppointmentsDialogComponent,
    ServiceImageUploadDialogComponent,
    AppointmentsPreviewComponent,
    ServiceProviderComponent,
    ServiceProviderDetailsInfoComponent,
  ],
  entryComponents: [
    AdminDialogComponent,
    ProfileComponent,
    HelpComponent,
    AppointmentsPreviewComponent,
    ServiceListDialogComponent,
    AppointmentsDialogComponent,
    ServiceImageUploadDialogComponent,
    ServiceProviderDetailsInfoComponent
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
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatNativeDateModule,
    ChartModule,
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
    Ng2OdometerModule,
    MatStepperModule,
    MatTooltipModule,
   // AppointmentsPreviewComponent,
    ToasterModule.forRoot(),
    RouterModule.forRoot(routes)
  ],
  providers: [
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
    GoogleMapLoaderService.load().then(() => {});
    if (
      localStorage.getItem(AUTHGWCONSTANTS.bearerToken) === 'null' ||
      localStorage.getItem(AUTHGWCONSTANTS.bearerToken) === null
    ) {
      localStorage.removeItem(AUTHGWCONSTANTS.bearerToken);
      this.router.navigate(['admin/sign_in']);
    } else {
      this.router.navigate(['admin/dashboard']);
    }
  }
}
