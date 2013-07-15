(defadvice point-min (around around-point-min-advice)
  "" my-global-marker-min)
(defadvice point-max (around around-point-max-advice)
  "" my-global-marker-max)

(defun deactivate-narrowing ()
  ""
  (setq my-global-marker-min nil)
  (setq my-global-marker-max nil)
  (ad-deactivate 'point-max)
  (ad-deactivate 'point-min))

(defun activate-narrowing (min max)
  ""
  (setq my-global-marker-min min)
  (setq my-global-marker-max max)
  (ad-activate 'point-max)
  (ad-activate 'point-min))

(defun try-narrow ()
  ""
  (activate-narrowing 
   (region-beginning) 
   (region-end)
   ))
