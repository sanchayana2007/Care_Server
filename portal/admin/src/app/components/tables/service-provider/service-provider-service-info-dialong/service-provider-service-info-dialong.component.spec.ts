import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServiceProviderServiceInfoDialongComponent } from './service-provider-service-info-dialong.component';

describe('ServiceProviderServiceInfoDialongComponent', () => {
  let component: ServiceProviderServiceInfoDialongComponent;
  let fixture: ComponentFixture<ServiceProviderServiceInfoDialongComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServiceProviderServiceInfoDialongComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServiceProviderServiceInfoDialongComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
