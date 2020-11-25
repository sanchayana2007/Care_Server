import { AuthorizationComponent } from './authorization/authorization.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ServiceOptionsComponent } from './authorization/service-options/service-options.component';
import { DetailsPageComponent } from './components/account/details-page/details-page.component';
import { MyServicesComponent} from './components/account/my-services/my-services.component';
import { MyBookingsComponent } from './components/account/my-bookings/my-bookings.component';
import { ServiceProviderComponent } from './components/account/service-provider/service-provider.component';
const appRoutes: Routes = [
  {
    path: '',
    component: AuthorizationComponent,
    children: [
      {
        path: 'service-types',
        component: ServiceOptionsComponent
      },
      {
        path: 'account/details-page',
        component: DetailsPageComponent
      },
      {
        path: 'account/service-provider',
        component: ServiceProviderComponent
      },
      {
        path: 'account/my-services',
        component: MyServicesComponent
      },
      {
        path: 'account/my-bookings',
        component: MyBookingsComponent
      },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
