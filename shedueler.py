def shortest_time_remaining(processes=[]):
  arrival_times = sorted(set(map(lambda (a,b,c,d): c, processes)))
  currently_running = None
  quantums = 0
  while True:
    if (len(arrival_times) and quantums == arrival_times[0]):
      arrival_times = arrival_times[1:]
      if currently_running:
        processes.append(currently_running)
      currently_running = None

    if currently_running == None:
      available_processes = [(a,b,c,d) for (a,b,c,d) in processes if c <=
        quantums]
      if available_processes:
        currently_running = min(available_processes, key = lambda (a,b,c,d): d)
        processes.remove(currently_running)
      else:
        print "No processes running at time", quantums
        quantums += 1
        continue

    name, user, starttime, remaining = currently_running
    remaining -= 1

    print "At time %i" % int(quantums),
    print name, "remaining time:", remaining

    if remaining:
      currently_running = (name, user, starttime, remaining)
    else:
      currently_running = None
      print "process %s has finished" % name

    quantums +=1

    if currently_running == None and len(processes) == 0:
      break

shortest_time_remaining([("A","Mohamed",1,3), ("B","Mohamed",2,1),
("C","Mohamed",3,1), ("D","Mohamed",8,3)])
