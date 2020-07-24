import { TestBed } from '@angular/core/testing';

import { ServiceOptionsService } from './service-options.service';

describe('ServiceOptionsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ServiceOptionsService = TestBed.get(ServiceOptionsService);
    expect(service).toBeTruthy();
  });
});
