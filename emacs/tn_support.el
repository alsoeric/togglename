;; support file for toggle name functions when interacting with Emacs environment.


(defun write-region-clippy ()
  ""
  ;; write region to a file
  (write-region
   (region-beginning) 
   (region-end)
   "~/tn_clippy.txt"
   )
)

(defun write-clippy ()
  "write last kill ring entry"
  (with-temp-buffer (yank)(write-region-clippy)))

(defun read-clippy ()
  ""
  (insert-file-contents 
      "~/tn_clippy.txt"
      )
)

(defun use-this-region-pre()
  "follow with toggle-name-post"
  (kill-region
   (region-beginning) 
   (region-end)
   )
  (write-clippy)
  )

(defun toggle-name-pre()
  "follow with toggle-name-post"
  (insert "\C-a")
  (kill-whole-line)
  (write-clippy)
  )

(defun toggle-name-post () 
  ""
  (read-clippy)  ;;(yank) ;; overwrites active region ??
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
  (write-clippy)
  )

(defun toggle-expression-pre () 
  "follow with toggle-post"
  (py-kill-expression)
  (write-clippy)
  )

(defun toggle-class-pre () 
  "follow with toggle-post"
  (py-kill-class)
  (write-clippy)
  )

(defun toggle-def-pre () 
  "follow with toggle-post"
  (py-kill-def)
  (write-clippy)
  )

(defun toggle-post () 
  ""
   (narrow-to-region    
    (region-beginning) 
    (region-end)
    )
   (read-clippy)  ;; (yank) ;; overwrites active region ??
   )

(defun fix-pre ()
  "common fix code. works in narrowed region"
  (kill-region (point-min) (point-max))
  (write-clippy)
  )

(defun fix-cleanup ()
   ""
   (read-clippy)   ;; (yank)
   ;; search forward for cursor marker
   (beginning-of-buffer)
   (search-forward "\C-a" nil t)
   (delete-backward-char 1)		  
   )
