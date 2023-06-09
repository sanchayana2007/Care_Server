import { LiveTrackComponent } from './components/live-track/live-track.component';
import { AuthorizationComponent } from './authorization/authorization.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AdminComponent } from './components/tables/admin/admin.component';
import { ServiceListComponent } from './components/tables/service-list/service-list.component';
import { AppointmentsComponent } from './components/tables/appointments/appointments.component';
import {ServiceProviderComponent} from './components/tables/service-provider/service-provider.component';
import {UsersComponent} from './components/tables/users/users.component';
import {NotificationsComponent} from './components/tables/notifications/notifications.component';
import {ProdectsComponent} from './components/tables/prodects/prodects.component';
import { SmsComponent} from './components/tables/sms/sms.component';
const appRoutes: Routes = [
  {
    path: 'admin',
    component: AuthorizationComponent,
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'live_track',
        component: LiveTrackComponent
      },
      {
        path: 'table/resource/admin',
        component: AdminComponent
      },
      {
        path: 'table/service-list',
        component: ServiceListComponent
      },
      {
        path: 'table/appointments',
        component: AppointmentsComponent
      },
      {
        path: 'table/users',
        component: UsersComponent
      },
      {
        path: 'table/service-provider',
        component: ServiceProviderComponent
      },
      {
        path: 'table/notifications',
        component: NotificationsComponent
      },
      {
        path: 'table/prodects',
        component: ProdectsComponent
      },
      {
        path: 'table/sms',
        component: SmsComponent
      },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
