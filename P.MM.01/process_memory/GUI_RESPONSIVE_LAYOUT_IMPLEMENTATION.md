# GUI responsive layout implementation

Дата: 2026-08-25.

## Scope

Исправлена обрезка правой части универсального wxPython GUI при уменьшении
главного окна. Реализация GUI Continue/Open для transaction-session snapshot не
начиналась. Application Facade, drafts, session snapshot/restore/lifecycle,
Body/XML и нормативная модель P.MM.01 не изменялись.

## Root cause audit

- `MainFrame` имел жёсткий minimum size `900x650`.
- `FormPanel` создавался только с `wx.VSCROLL`; правый контент был недоступен.
- Filter и action bars использовали один горизонтальный `BoxSizer`.
- Длинные status/summary texts не пересчитывали перенос при resize.
- Корневые panel/notebook/form sizers уже использовали `wx.EXPAND`; absolute
  positioning не обнаружено.
- Field captions находятся над inputs. Binary row сохраняет растягиваемое имя,
  выбор, очистку и info; fallback-доступ обеспечивает горизонтальная прокрутка.
- Validation `ListCtrl` сохраняет свою горизонтальную прокрутку длинных колонок.

## Implementation

- Minimum frame size: `700x560`; стартовый размер не меньше `760x600` при
  достаточной площади экрана.
- `FormPanel`: `wx.HSCROLL | wx.VSCROLL`, scroll rate по обеим осям и deferred
  `Layout()/FitInside()` после resize.
- Filter, data action и XML action bars переведены на `wx.WrapSizer`.
- Status, form summary и validation summary оборачиваются по ширине data tab.
- Callback допускает ранние resize events и использует только созданные controls.

## Verification

- Baseline: engine 172 tests / 790 subtests; P.MM.01 56 / 71; engine GUI 11;
  P.MM.01 GUI 13. Итого 252 tests / 861 subtests — PASS.
- Final existing suites: engine 172; P.MM.01 56; engine GUI 11; P.MM.01 GUI 13 — PASS.
- Новый real-wx regression: 1 — PASS.
- macOS resize `1200x800 -> 900x650 -> 700x560 -> 1100x760` — `WX_RESIZE_SMOKE_OK`.
- Compile check изменённых GUI modules — PASS.

## Status

GUI_RIGHT_SIDE_CLIPPING_FIXED = YES

RESPONSIVE_FORM_LAYOUT = YES

HORIZONTAL_CONTENT_ACCESSIBLE = YES

VERTICAL_CONTENT_ACCESSIBLE = YES

BINARY_CONTROL_RESIZE_SAFE = YES

WX_RESIZE_SMOKE = PASS

MACOS_RESIZE_SMOKE = PASS

SAFE_TO_PROCEED_WITH_GUI_SESSION_CONTROLS = YES
