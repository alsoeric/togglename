;; support file for toggle name functions when interacting with Emacs environment.

;; savemp():= {ctrl+x}r{space}z{ctrl+x}{ctrl+x}{ctrl+x}r{space}a;

;; restoremp() := {ctrl+x}rjz{ctrl+shift+2}{ctrl+x}rja;



(defun toggle-name-pre()
  "follow with toggle-name-post"
  (insert "\C-a")
  (kill-whole-line)
  )

(defun toggle-name-post () 
  ""
  (yank) ;; overwrites active region ??
  (narrow-to-region    
    (region-beginning) 
    (region-end)
    )
  ;; search for C-a and stop
  (search-forward "\C-a")
  (delete-backward-char 1)
  )

(defun toggle-statement-pre () 
  "follow with toggle-post"
  (py-kill-statement)
  )

(defun toggle-expression-pre () 
  "follow with toggle-post"
  (py-kill-expression)
  )

(defun toggle-class-pre () 
  "follow with toggle-post"
  (py-kill-class)
  )

(defun toggle-def-pre () 
  "follow with toggle-post"
  (py-kill-def)
  )

(defun toggle-post () 
  ""
   (yank) ;; overwrites active region ??
   (narrow-to-region    
    (region-begin) 
    (region-end)
    )
   )

(defun fix-pre ()
  "common fix code. works in narrowed region"
  (kill-region (point-min) (point-max))
  )

(defun fix-cleanup ()
   ""
   (yank)
   ;; search forward for cursor marker
   (beginning-of-buffer)
   (search-forward "\C-a")
   (delete-backward-char 1)		  
   )
