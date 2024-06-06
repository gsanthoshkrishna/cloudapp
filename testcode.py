def a():
    #select  res_prop_id from resource_prop where prop_name = 'name' and  res_id = 3
    p_name = 'name'
    r_id ='3'
    query = "select  res_prop_id from resource_prop where prop_name = '" + p_name + "' and  res_id = " + r_id 
    print(query)

    num = "1"
    #these are 2s factors
    #these are 5s factors
    #these are 11s factors
    temp = "these are " + num + "s"
    print(temp)
    


a()

  
