import { LiveTrackComponent } from './components/live-track/live-track.component';
import { AuthorizationComponent } from './authorization/authorization.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AdminComponent } from './components/tables/admin/admin.component';
import { ServiceListComponent } from './components/tables/service-list/service-list.component';
import { AppointmentsComponent } from './components/tables/appointments/appointments.component';

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
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
