
(defun toggle-region ()
  "selected region will be toggleed and replaced"
  (interactive)
  (shell-command-on-region (region-beginning) (region-end) "python ~/Documents/GitHub/togglename/vocola/extensions/vocola_ext_togglename.py -mst" t)
)


(defun potato-region ()
  "seleced region will be potatoed"
  (interactive)
  (shell-command-on-region (region-beginning) (region-end) "python potato.py" t)
)


; to find top of narrowed buffer use (point-min) and (point-max)
