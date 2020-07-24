import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GoogleMapCanvasComponent } from './google-map-canvas.component';

describe('GoogleMapCanvasComponent', () => {
  let component: GoogleMapCanvasComponent;
  let fixture: ComponentFixture<GoogleMapCanvasComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GoogleMapCanvasComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GoogleMapCanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
