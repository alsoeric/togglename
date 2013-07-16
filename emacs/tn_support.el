;; support file for toggle name functions when interacting with Emacs environment
;;; --------------------------------------------
;Narrowing
(defun narrow-to-region-in-other-window (start end)
  "Narrow region in another window"
  (interactive "r")
  (deactivate-mark)
  (let ((buf (clone-indirect-buffer nil nil)))
    (with-current-buffer buf
      (narrow-to-region start end))
      (switch-to-buffer-other-window buf))) 


(defun narrow-to-region-in-other-frame (start end)
  "Narrow region in another frame"
  (interactive "r")
  (deactivate-mark)
  (let ((buf (clone-indirect-buffer nil nil)))
    (with-current-buffer buf
      (narrow-to-region start end))
      (switch-to-buffer-other-frame buf))
) 
;;;-------------------------
; emacs.vcl macro traslates

(defun tn-class-pre () (interactive)
  "Narrow class in another frame kill all"
  (interactive)
  (deactivate-mark)
  (let ((buf (clone-indirect-buffer nil nil)))
    (with-current-buffer buf
      (narrow-to-region (py-beginning-of-class-position) (py-end-of-class-position))
      (insert "\C-a")
      (kill-region (point-min) (point-max))
      )
    (switch-to-buffer-other-frame buf))
) 

(defun tn-def-pre () (interactive)
  "Narrow class in another frame kill all"
  (interactive)
  (deactivate-mark)
  (let ((buf (clone-indirect-buffer nil nil)))
    (with-current-buffer buf
      (narrow-to-region (py-beginning-of-def-position) (py-end-of-def-position))
      (insert "\C-a")
      (kill-region (point-min) (point-max))
      )
    (switch-to-buffer-other-frame buf))
) 

(defun tn-fix-unknown-pre () (interactive)
  "kill whole region"
  (kill-region (point-min) (point-max))
)

(defun tn-post () (interactive)
  "retrive region from kill buffer, look for cursor marker"
  (yank)
  (exchange-point-and-mark)
  (search-forward "\C-a" nil t 1)
  (delete-backward-char 1)
  ;(if ( equal (point) (point-max)) ; and if indirect buffer
  ;   (message "at end of buff");tn-kill-frame-and-narrowed-buffer) ; kill buffer & frame. ;should have the narrowed buffer name have a char in it.
  ; )
)

(defun tn-kill-frame-and-narrowed-buffer () (interactive)
  "kills the narrwed buffer and deletes the frame"
  (kill-buffer)
  (delete-frame) ;
)











































(defun toggle-region (start end)
  "selected region will be toggleed and replaced"
  (interactive "r")
  (shell-command-on-region (start) (end) "python ~/Documents/GitHub/togglename/vocola/extensions/vocola_ext_togglename.py -mst" t)
)

(defun toggle-buffer () (interactive)
  "toggle the whole buffer"
  (toggle-region (point-min) (point-max))
)

;(defun tn-toggle-def-or-class () (interactive)
;  ((narrow-frame-def-or-class)
;   
;   ...
;;;-------------------------
; emacs.vcl macro traslate

(defun tncleanup () (interactive)
 "Search forward, delete cursor mark. Return t if point == point-end"
 (yank)
 (exchange-point-and-mark)
  ;; search forward for cursor marker
 (search-forward "\C-a")
 (delete-backward-char 1)
 (if ( equal (point) (point-max)) ; and if indirect buffer
     t ; kill buffer & frame. ;should have the narrowed buffer name have a char in it.
   )
)

