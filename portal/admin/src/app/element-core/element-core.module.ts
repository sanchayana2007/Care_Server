import { NgModule } from '@angular/core';
import { FullscreenComponent } from './fullscreen/fullscreen.component';
import { SearchBarComponent } from './search-bar/search-bar.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { SidemenuComponent } from './sidemenu/sidemenu.component';
import { SidemenuItemComponent } from './sidemenu-item/sidemenu-item.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { ToolbarNotificationComponent
  } from './toolbar-notification/toolbar-notification.component';
import { UserMenuComponent } from './user-menu/user-menu.component';

import { MatListModule } from '@angular/material/list';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTabsModule, MatCardModule, MatTooltipModule } from '@angular/material';
import { PerfectScrollbarModule } from 'ngx-perfect-scrollbar';
import { PERFECT_SCROLLBAR_CONFIG } from 'ngx-perfect-scrollbar';
import { PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
import { FlexLayoutModule } from '@angular/flex-layout';
import { RouterModule } from '@angular/router';
import {
  MatSidenavModule,
  MatSliderModule,
  MatProgressBarModule
} from '@angular/material';
import { DashCardVerticalComponent } from './dash-card-vertical/dash-card-vertical.component';
import { Ng2OdometerModule } from 'ng2-odometer';

const DEFAULT_PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
  suppressScrollX: true
};

@NgModule({
  declarations: [
    FullscreenComponent,
    SearchBarComponent,
    SidebarComponent,
    SidemenuComponent,
    SidemenuItemComponent,
    ToolbarComponent,
    ToolbarNotificationComponent,
    UserMenuComponent,
    DashCardVerticalComponent
  ],
  imports: [
    MatListModule,
    MatCardModule,
    MatTooltipModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    PerfectScrollbarModule,
    FlexLayoutModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatSidenavModule,
    MatTabsModule,
    MatSliderModule,
    MatInputModule,
    MatProgressBarModule,
    RouterModule,
    Ng2OdometerModule
  ],
  exports: [
    SidemenuComponent,
    SidemenuItemComponent,
    ToolbarNotificationComponent,
    ToolbarComponent,
    SearchBarComponent,
    FullscreenComponent,
    SidebarComponent,
    UserMenuComponent,
    DashCardVerticalComponent
  ],
  providers: [
    {
      provide: PERFECT_SCROLLBAR_CONFIG,
      useValue: DEFAULT_PERFECT_SCROLLBAR_CONFIG
    }
  ]
})
export class ElementCoreModule {

 }
