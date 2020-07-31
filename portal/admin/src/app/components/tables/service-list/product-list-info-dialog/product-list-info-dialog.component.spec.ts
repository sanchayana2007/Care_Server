import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductListInfoDialogComponent } from './product-list-info-dialog.component';

describe('ProductListInfoDialogComponent', () => {
  let component: ProductListInfoDialogComponent;
  let fixture: ComponentFixture<ProductListInfoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductListInfoDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductListInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
