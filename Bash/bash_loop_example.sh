for i in 0.02 0.04 0.06 0.08 0.10 0.12 0.14 0.16 0.18 0.20
do
    echo "$i" | xargs -i java -jar StegExpose.jar ../images/imagenet_1k/gt_and_hips/ fast {} ./report/imagenet_1k/hips/{}.csv
    echo "HIPS $i done!"
done

for i in 0.02 0.04 0.06 0.08 0.10 0.12 0.14 0.16 0.18 0.20
do
    echo "$i" | xargs -i java -jar StegExpose.jar ../images/imagenet_1k/gt_and_isn/ fast {} ./report/imagenet_1k/isn/{}.csv
    echo "ISN $i done!"
done