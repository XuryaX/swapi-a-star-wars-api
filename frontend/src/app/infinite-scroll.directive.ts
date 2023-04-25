import { Directive, ElementRef, HostListener, Input, Output, EventEmitter } from '@angular/core';

@Directive({
  selector: '[appInfiniteScroll]'
})
export class InfiniteScrollDirective {
  @Input() hasMore: boolean = false;
  @Output() scrolled = new EventEmitter<void>();

  constructor(private el: ElementRef) {}

  @HostListener('scroll')
  onScroll(): void {
    const scrollHeight = this.el.nativeElement.scrollHeight;
    const scrollTop = this.el.nativeElement.scrollTop;
    const clientHeight = this.el.nativeElement.clientHeight;

    if (scrollTop + clientHeight >= scrollHeight - 1 && this.hasMore) {
      this.scrolled.emit();
    }
  }
}
