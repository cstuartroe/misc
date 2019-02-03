import java.util.*;

class Collatz {
    static HashMap<Long,Integer> hailstones;
    
    static Integer hail(Long stone, boolean isprint) {
        LinkedList<Long> stones = new LinkedList<Long>();
        Long curr = stone;
        while(! hailstones.containsKey(curr)) {
            if (isprint) { System.out.println(curr); }
            Long next;
            if (curr % 2 == 0) {
                next = curr/2;
            } else{
                next = curr*3+1;
            }
            stones.addFirst(curr);
            curr = next;
        }
        Integer base_steps = hailstones.get(curr);
        curr = stones.pollFirst();
        Integer trace = 1;
        while (curr != null) {
            hailstones.put(curr, base_steps + trace);
            trace++;
            curr = stones.pollFirst();
        }
        return hailstones.get(stone);
    }
    
    public static void main(String[] args) {
        hailstones = new HashMap<Long,Integer>();
        hailstones.put(new Long(1),0);
        Integer max_steps = 0;
        Long max_stone = new Long(0);
        Long limit = new Long(5_000_000);
        for (Long stone = new Long(2); stone < limit; stone++) {
            if ((stone*10)%limit == 0) { System.out.println("Doing " + stone); }
            Integer steps = hail(stone, false);
            if (steps > max_steps) {
                max_steps = steps;
                max_stone = stone;
            }
        }
        System.out.println(max_stone + " " + max_steps);
    }
}