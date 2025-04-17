(define (curry-cook formals body) 
(if (null? formals)
body  ; if no body,return body
(let ((param (car formals)))  ; car first formals
  (list 'lambda (list param)  ; new lambda
        (curry-cook (cdr formals) body)))))  
        ; Recursively process the remaining parameters

(define (curry-consume curry args);get args,return lambda
(if (null? args)  
curry                  
(curry-consume         
    (curry (car args))  
    (cdr args)          
)))

(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))

(define (cadr lst) (car (cdr lst)))

(define (switch-to-cond switch-expr)
  (cons 'cond
        (map (lambda (option)
               (cons (list 'equal? (cadr switch-expr) (car option))(cdr option)))
             (car (cdr (cdr switch-expr))))))
