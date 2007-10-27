#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/mozilla-sunbird"

MOZARGS=
MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $LIBDIR/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo ${MOZILLA_FIVE_HOME}/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

if [ -n "$MOZARGS" ]; then
	SUNBIRD="$LIBDIR/sunbird $MOZARGS"
else
	SUNBIRD="$LIBDIR/sunbird"
fi

exec $SUNBIRD "$@"
