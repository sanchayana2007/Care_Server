import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServiceProviderDetailsInfoComponent } from './service-provider-details-info.component';

describe('ServiceProviderDetailsInfoComponent', () => {
  let component: ServiceProviderDetailsInfoComponent;
  let fixture: ComponentFixture<ServiceProviderDetailsInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServiceProviderDetailsInfoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServiceProviderDetailsInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
