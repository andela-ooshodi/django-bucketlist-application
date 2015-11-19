from bucketlist.models import BucketList, BucketlistItem
from apiv1.serializer import BucketListSerializer, BucketItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BucketListView(APIView):

    """
    List all buckets, or create a new bucket.
    """

    # gets all buckets from the database

    def get(self, request):
        """
        List all buckets that belong to you
        """
        buckets = BucketList.objects.filter(author_id=self.request.user)
        serializer = BucketListSerializer(buckets, many=True)
        return Response(serializer.data)

    # creates a new bucket
    def post(self, request):
        """
        Create a new bucket
        ---
        parameters:
            - name: name
              description: name of bucket to create
              required: true
              type: string
              paramType: form
        """
        serializer = BucketListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListDetailView(APIView):

    """
    Retrieve, Update or delete a bucketlist
    """

    # checks the bucket exists in the database

    def get_object(self, bucketlistid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        if bucket:
            return bucket
        else:
            raise Http404

    # gets the bucket
    def get(self, request, bucketlistid):
        """
        Retrieve a bucket
        """
        bucket = self.get_object(bucketlistid)
        serializer = BucketListSerializer(bucket)
        return Response(serializer.data)

    # edit bucket
    def put(self, request, bucketlistid):
        """
        Edit an already created bucket
        ---
        parameters:
            - name: name
              description: change the name of bucket
              required: true
              type: string
              paramType: form
        """
        bucket = self.get_object(bucketlistid)
        serializer = BucketListSerializer(bucket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete bucket
    def delete(self, request, bucketlistid):
        """
        Delete a bucket
        """
        bucket = self.get_object(bucketlistid)
        bucket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BucketItemView(APIView):

    """
    Create a bucketitem
    """

    # checks the bucketlist for the bucketitem exists

    def get_object(self, bucketlistid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        if bucket:
            return bucket
        else:
            raise Http404

    # adds a new bucketitem
    def post(self, request, bucketlistid):
        """
        Create a new bucketitem
        ---
        parameters:
            - name: name
              description: name of bucketitem to create
              required: true
              type: string
              paramType: form
        """
        bucket = self.get_object(bucketlistid)
        serializer = BucketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bucketlist_id=bucket.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketItemDetailView(APIView):

    """
    Retrieve, Update or delete a bucketitem
    """

    # checks the bucketitem exists

    def get_object(self, bucketlistid, bucketitemid):
        bucket = BucketList.objects.filter(
            pk=bucketlistid,
            author_id=self.request.user).first()
        bucketitem = BucketlistItem.objects.filter(
            pk=bucketitemid, bucketlist_id=bucket).first()
        if bucket and bucketitem:
            return bucketitem
        else:
            raise Http404

    # get a bucketitem
    def get(self, request, bucketlistid, bucketitemid):
        """
        Retrieve a bucketitem from a bucket you own
        """
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        serializer = BucketItemSerializer(bucketitem)
        return Response(serializer.data)

    # edit a bucketitem
    def put(self, request, bucketlistid, bucketitemid):
        """
        Edit a bucketitem from a bucket you own

        To test marking this item as done functionality,
        postman can be used instead
        ---
        parameters:
            - name: name
              description: change name of bucketitem
              required: false
              type: string
              paramType: form
        """
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        if 'name' not in request.data.keys():
            request.data['name'] = bucketitem.name
        serializer = BucketItemSerializer(bucketitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a bucketitem
    def delete(self, request, bucketlistid, bucketitemid):
        """
        Delete a bucketitem from a bucket you own
        """
        bucketitem = self.get_object(bucketlistid, bucketitemid)
        bucketitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
