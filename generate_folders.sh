for i in $(seq -f "%03g" 0 100); do
    for j in $(seq -f "%02g" 0 30); do
        mkdir -p "$i/$j"
    done
done

# Location: 77/12
