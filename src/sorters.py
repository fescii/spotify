from typing import List, Dict


def bubble_sort(data: List[Dict], key: str, ascending: bool = True) -> List[Dict]:
    """
    Implementation of bubble sort algorithm

    Args:
        data (List[Dict]): List of dictionaries to sort
        key (str): Dictionary key to sort by
        ascending (bool): Sort in ascending order if True

    Returns:
        List[Dict]: Sorted list of dictionaries
    """
    data = data.copy()  # Make a copy to avoid modifying the original
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if ascending:
                if data[j][key] > data[j + 1][key]:
                    data[j], data[j + 1] = data[j + 1], data[j]
            else:
                if data[j][key] < data[j + 1][key]:
                    data[j], data[j + 1] = data[j + 1], data[j]
    return data


def quick_sort(data: List[Dict], key: str, ascending: bool = True) -> List[Dict]:
    """
    Implementation of quicksort algorithm

    Args:
        data (List[Dict]): List of dictionaries to sort
        key (str): Dictionary key to sort by
        ascending (bool): Sort in ascending order if True

    Returns:
        List[Dict]: Sorted list of dictionaries
    """
    if len(data) <= 1:
        return data

    pivot = data[len(data) // 2]
    pivot_val = pivot[key]

    left = [x for x in data if x[key] < pivot_val]
    middle = [x for x in data if x[key] == pivot_val]
    right = [x for x in data if x[key] > pivot_val]

    if ascending:
        return (
            quick_sort(left, key, ascending)
            + middle
            + quick_sort(right, key, ascending)
        )
    else:
        return (
            quick_sort(right, key, not ascending)
            + middle
            + quick_sort(left, key, not ascending)
        )


def merge_sort(data: List[Dict], key: str, ascending: bool = True) -> List[Dict]:
    """
    Implementation of merge sort algorithm.

    Args:
        data (List[Dict]): List of dictionaries to sort
        key (str): Dictionary key to sort by
        ascending (bool): Sort in ascending order if True

    Returns:
        List[Dict]: Sorted list of dictionaries
    """
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], key, ascending)
    right = merge_sort(data[mid:], key, ascending)

    return merge(left, right, key, ascending)


def merge(left: List[Dict], right: List[Dict], key: str, ascending: bool) -> List[Dict]:
    """
    Helper function for merge sort

    Args:
        left (List[Dict]): Left list to merge
        right (List[Dict]): Right list to merge
        key (str): Dictionary key to sort by
        ascending (bool): Sort in ascending order if True

    Returns:
        List[Dict]: Merged and sorted list of dictionaries
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if ascending:
            if left[i][key] <= right[j][key]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left[i][key] >= right[j][key]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
