```json
  "in_folder": "test/INPUT",
  "out_folder": "test/OUTPUT",
  "max_workers": 4,
  "processed": []
```
- in_folder - directory where the images come from
- out_folder - directory where the main image is
- max_workers - maximum number of threads default(min(32, cpu_count() + 4))
- processed - queue of processes, more on them later

``` json
  "processed": [
    {
      "type": "sharp",
      "diapason_white": -1,
      "diapason_black": -1,
      "high_input": 255,
      "low_input": 0,
      "gamma": 1.0,
      "cenny": false
    },
    {
      "type": "screentone",
      "dot_size": 7
    },
    {
      "type": "resize",
      "size": 2000,
      "interpolation": "linear",
      "width": true,
      "percent": 100,
      "spread": true,
      "spread_size": 2800,
      "color_fix": true,
      "gamma_correction": false
    }
  ]
```
- type: [sharp, screentone, resize] - process type, one of the listed
  - type: sharp
    - diapason_white - removes noise using medial blur and, using the set value, creates a mask that is superimposed in pure white on the image default(-1) -1 this is disabled
    - diapason_black - the process of expanding the contours, quite outdated and rarely needed, I advise you not to touch default(-1) -1 this is disabled
    - high_input, low_input, gamma - standard levels default(0, 255,1.0)
    - canny - Applying a canny filter to their image helps to get rid of wavy outlines due to highlighting at the edges default(false)
  - type: screentone
    - dot_size - maximum screentone dot size default(7)
  - type: resize
    - size - value by which the scan will be reduced
    - interpolation: ['nearest', 'linear', 'cubic_catrom', 'cubic_mitchell', 'cubic_bspline', 'lanczos', 'gauss', 'lagrange'] default('linear')
    - width - Boolean value, if true size is wide, if false it is height default(false)
    - percent - reduction percentage if size is larger than the image size default(100)
    - spread - Boolean value when enabled, all spreads will be resized to fit spread_size, works with width enabled default(false)
    - spread_size - Dimensions of the spread with spread enabled default(2800)
    - color_fix - when resizing, some images have a grid on white, this is corrected by highlighting by 5 points; in fact, when set to true, it simply highlights by 5 points default(false)
    - gamma_correction - built-in function resize chainner ext gamma_correction default(false)


