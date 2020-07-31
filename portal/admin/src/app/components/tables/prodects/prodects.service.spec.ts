import { TestBed } from '@angular/core/testing';

import { ProdectsService } from './prodects.service';

describe('ProdectsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ProdectsService = TestBed.get(ProdectsService);
    expect(service).toBeTruthy();
  });
});
