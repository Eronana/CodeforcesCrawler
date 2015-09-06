cd html
for h in *.html;
do
    wkhtmltopdf -q "$h" "../pdf/`echo "$h"|sed "s/\.html/\.pdf/"`"
done
