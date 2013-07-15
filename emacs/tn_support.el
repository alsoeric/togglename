;; support file for toggle name functions when interacting with Emacs environment.

;; savemp():= {ctrl+x}r{space}z{ctrl+x}{ctrl+x}{ctrl+x}r{space}a;

;; restoremp() := {ctrl+x}rjz{ctrl+shift+2}{ctrl+x}rja;


;; (defun tncleanup ()
;;   ""
;;   (
;;    (exchange-point-and-mark)
;;    ;; search forward for cursor marker
;;    (search-forward "\C-a")
;;    (delete-backward-char 1)		  
;;    )
;; )

(defun toggle-statement-pre () 
  ""
  (py-kill-statement)
  ;; (yank)  ;; define region
  (narrow-to-region    
   (region-beginning) 
   (region-end))
  ;; ends here for return to vocola
  ;; toggle.name(1,0) 
  )

(defun toggle-statement-post () 
  ""
   (exchange-point-and-mark)
   (yank) ;; overwrites active region
   (exchange-point-and-mark)) ;; activate it again
