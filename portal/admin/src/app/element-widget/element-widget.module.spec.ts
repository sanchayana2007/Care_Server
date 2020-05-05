import { ElementWidgetModule } from './element-widget.module';

describe('ElementWidgetModule', () => {
  let elementWidgetModule: ElementWidgetModule;

  beforeEach(() => {
    elementWidgetModule = new ElementWidgetModule();
  });

  it('should create an instance', () => {
    expect(elementWidgetModule).toBeTruthy();
  });
});
