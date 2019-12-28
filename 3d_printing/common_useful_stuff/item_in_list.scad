
function remove_first(list) = (
                        len(list) < 2) ? [] :
                        [for (index=[1:len(list)-1]) list[index]];

function item_in_list(item, list) =
  (item == list[0]) ? true :
  (len(list) == 0 ? false :
   item_in_list(item, remove_first(list)));

echo(item_in_list([3,3], [[1,1],[1,2],[3,2]]));
