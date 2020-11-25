import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AppointmentsDialogComponent } from './appointments-dialog.component';

describe('AppointmentsDialogComponent', () => {
  let component: AppointmentsDialogComponent;
  let fixture: ComponentFixture<AppointmentsDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AppointmentsDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppointmentsDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
