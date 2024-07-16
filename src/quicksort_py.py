def quick_sort_algorithm(arr: list[int]) -> None:
    def _recursive_sort(items: list[int], low: int, high: int):
        if low < high:
            # Partition the array
            pivot_index = partition(items, low, high)
            # Recursively apply the quicksort to the sub-arrays
            _recursive_sort(items, low, pivot_index - 1)
            _recursive_sort(items, pivot_index + 1, high)

    def partition(items: list[int], low: int, high: int):
        pivot = items[high]  # Choose the last element as the pivot
        i = low - 1  # Pointer for the greater element
        for j in range(low, high):
            # If the current element is smaller than or equal to the pivot
            if items[j] <= pivot:
                i += 1  # Increment the pointer for the greater element
                items[i], items[j] = items[j], items[i]  # Swap
        items[i + 1], items[high] = (
            items[high],
            items[i + 1],
        )  # Swap the pivot element with the element at i + 1
        return i + 1  # Return the partitioning index

    _recursive_sort(arr, 0, len(arr) - 1)


def quick_sort(arr: list[int]) -> list[int]:
    quick_sort_algorithm(arr)
    return arr
