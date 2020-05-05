import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashCardComponent } from './dash-card/dash-card.component';
import { GraphCardComponent } from './graph-card/graph-card.component';
import { GoogleMapCanvasComponent } from './google-map-canvas/google-map-canvas.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule, MatIconModule, MatTabsModule,
  MatToolbarModule, MatListModule, MatChipsModule, MatCardModule } from '@angular/material';
import { Ng2OdometerModule } from 'ng2-odometer';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    FlexLayoutModule,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatToolbarModule,
    MatListModule,
    Ng2OdometerModule,
    MatCardModule,
    // RoundProgressModule,
    // MatMenuModule,
    MatChipsModule,
    // MatProgressBarModule,
    FormsModule,
    ReactiveFormsModule,
    // ChartsModule,
  ],
  declarations: [
    DashCardComponent,
    GraphCardComponent,
    GoogleMapCanvasComponent,
  ],
  exports: [
    DashCardComponent,
    GraphCardComponent,
    GoogleMapCanvasComponent,
  ]
})
export class ElementWidgetModule { }
