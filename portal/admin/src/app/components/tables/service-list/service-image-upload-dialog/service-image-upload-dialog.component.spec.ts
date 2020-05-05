import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServiceImageUploadDialogComponent } from './service-image-upload-dialog.component';

describe('ServiceImageUploadDialogComponent', () => {
  let component: ServiceImageUploadDialogComponent;
  let fixture: ComponentFixture<ServiceImageUploadDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServiceImageUploadDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServiceImageUploadDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
